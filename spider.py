# Made by foxsinofgreed1729
# Many thanks to Zaid Sabih and udemy.com

import requests
import re


def request_url(url):
    try:
        get_resp = requests.get("http://" + url)
        return get_resp
    except requests.exceptions.ConnectionError:
        pass


target = "bing.com"
response = request_url(target)
href_links = re.findall('(?:href=")(.*?)"', str(response.content))
for link in href_links:
    print(link)
