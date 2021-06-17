# Made by FoxSinOfGreed1729
# Many thanks to Zaid Sabih and Udemy.com
import requests


def request_url(url):
    try:
        get_resp = requests.get("http://" + url)
        return get_resp
    except requests.exceptions.ConnectionError:
        pass


def find_subdomains(file, target_url):
    with open(file, "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            test_url = word + target_url
            print(test_url)
            req_response = request_url(test_url)
            if req_response:
                print("[+] Discovered Subdomain --> " + test_url)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def find_directories(wordlist, target_url):
    for line in wordlist:
        word = line.strip()
        test_url = target_url + "/" + word
        req_response = request_url(test_url)
        if req_response:
            print("[+] Discovered Directory --> " + test_url)


def find_directories_recursive(content, target_url, n):
    i = 0
    while i < n:
        word = content[i].strip()
        test_url = target_url + "/" + word
        req_response = request_url(test_url)
        if req_response:
            print("[+] Discovered Directory --> " + test_url)
            find_directories_recursive(content, test_url, n)
        else:
            pass
        i = i + 1


def crawl(filename, target):
    count = file_len(filename)
    with open(filename, "r") as wordlist_file:
        file_content = wordlist_file.readlines()
        find_directories_recursive(file_content, target, count)
        find_subdomains(filename, target)
        find_directories(wordlist_file, target)


the_target_url = "127.0.0.1"
word_list = "sws.txt"
try:
    crawl(word_list, the_target_url)
except KeyboardInterrupt:
    print("Keyboard Interrupt. Quitting")
    exit(0)

