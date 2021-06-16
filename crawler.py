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
    test_url = ""
    i = 0
    while i < n:
        word = content[i].strip()
        # print("Word\t" + word)
        test_url = target_url + "/" + word
        req_response = request_url(test_url)
        if req_response:
            print("[+] Discovered Directory --> " + test_url)
            # if test_url[-1] == ".":
            #     print("breaking")
            #     break
            find_directories_recursive(content, test_url, n)
        else:
            pass
        i = i + 1
    # print("exiting function from " + test_url)


target = "127.0.0.1"
filename = "sw.txt"
count = file_len(filename)
with open(filename, "r") as wordlist_file:
  file_content = wordlist_file.readlines()
  find_directories_recursive(file_content, target, count)
  find_directories(wordlist_file, target)
  find_subdomains(wordlist_file, target)
  
