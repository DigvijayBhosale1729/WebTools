# Made by foxsinofgreed1729
# Many thanks to Zaid Sabih and udemy.com

import requests
import re
import urllib.parse as urlparse


def request_url(url):
    try:
        get_resp = requests.get(url)
        return get_resp
    except requests.exceptions.ConnectionError:
        pass


def extract_links(url):
    response = request_url(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))


def unique_links(target):
    links = []
    href_links = extract_links(target)
    for link in href_links:
        link = urlparse.urljoin(target, link)
        if "#" in link:
            link = link.split("#")[0]
            # because links that have # are reference to a different part in the same page
        if target in link and link not in links:
            print(link)
            links.append(link)
    return links


target_url = "https://zsecurity.org"
crawled_urls = unique_links(target_url)
