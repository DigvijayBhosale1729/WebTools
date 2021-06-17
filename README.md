# WebTools
A suite of tools for in Vulnerability Assessment, Crawling, and Information Gathering.

## Editing crawler.py to set target and wordlist
```
target = "127.0.0.1"
filename = "sw.txt"
# change the target to the website you want to enumerate
# change filename to the wordlist that you're using
# in case the wordlist is in a different folder, put in the full path

# in case you want only a specific function to work, edit the crawl function
def crawl(filename, target):
    count = file_len(filename)
    with open(filename, "r") as wordlist_file:
        file_content = wordlist_file.readlines()
        find_directories_recursive(file_content, target, count)
        find_subdomains(filename, target)
        find_directories(wordlist_file, target)
# and comment out whatever function you dont want to use
```

## Editing spider.py to set target
```
target = "bing.com"
# change the target to the website you want href links from
```

## Usage

To use ```crawler.py```
```
python3 crawler.py
```
To use ```spider.py```
```
python3 spider.py
```
