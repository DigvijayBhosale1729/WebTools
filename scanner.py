import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.links = []
        self.links_to_ignore = ignore_links
        # so that we don't accidentally log out when crawling for links

    def extract_links(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', str(response.content))

    def crawl_links(self, target="CalledWithoutArgs"):
        if target == "CalledWithoutArgs":
            target = self.target_url
        # reason for doing this is so that you can call crawl links without args as well
        # if no args, then, it will use self.target_url

        href_links = self.extract_links(target)
        for link in href_links:
            link = urlparse.urljoin(target, link)
            if "#" in link:
                link = link.split("#")[0]
                # because links that have # are reference to a different part in the same page
            if target in link and link not in self.links and link not in self.links_to_ignore:
                self.links.append(link)
                self.crawl_links(link)

        return self.links

    def extract_forms(self, target="CalledWithoutArgs"):
        if target == "CalledWithoutArgs":
            target = self.target_url
        response = self.session.get(target)
        parsed_html = BeautifulSoup(response.content, "html.parser")
        form_list = parsed_html.findAll("form")
        return form_list

    def submit_form(self, form, value, target="CalledWithoutArgs"):
        if target == "CalledWithoutArgs":
            target = self.target_url
        action = form.get("action")
        post_url = urlparse.urljoin(target, action)
        method = form.get("method")

        web_data = {}
        input_list = form.findAll("input")
        for the_input in input_list:
            input_name = the_input.get("name")
            input_type = the_input.get("type")
            input_value = the_input.get("value")
            # we need input type because we need to know what to do
            # cant fill a submit button with txt, can we?
            if input_type == "text":
                input_value = value

            web_data[input_name] = input_value

        results = ""
        if method == "post":
            results = self.session.post(post_url, data=web_data)
        elif method == "get":
            results = self.session.get(post_url, params=web_data)
        return results

    def run_scanner(self):
        self.crawl_links()
        for link in self.links:
            forms = self.extract_forms(link)
            if "=" in str(link):
                print("[+] Testing " + link)
                xss_vulns = self.xss_in_form(form, link)
                for xss_vuln in xss_vulns:
                    print("\n\n[***] Xss vuln\t" + xss_vuln)

            for form in forms:
                print("[+] Testing form in " + link)
                xss_vulns = self.xss_in_form(form, link)
                for xss_vuln in xss_vulns:
                    print("\n\n[***] Xss vuln\t" + xss_vuln)

    def xss_in_form(self, form, target="CalledWithoutArgs"):
        if target == "CalledWithoutArgs":
            target = self.target_url
        results = []
        with open("xss.txt", "r") as script_list:
            for line in script_list:
                xss_script = line.strip()
                response = self.submit_form(form, xss_script, target)
                print("[+] Trying\t" + xss_script)
                if xss_script in str(response.content):
                    results.append(xss_script)
                    print("[***] Found XSS Vuln\t" + xss_script)
        return results

    def xss_in_link(self, url="CalledWithoutArgs"):
        if url == "CalledWithoutArgs":
            target = self.target_url
        results = []
        with open("xss.txt", "r") as script_list:
            for line in script_list:
                xss_script = line.strip()
                url = url.replace("=", "="+xss_script)
                response = self.session.get(url)
                print("[+] Trying\t" + xss_script)
                if xss_script in str(response.content):
                    results.append(xss_script)
                    print("[***] Found XSS Vuln\t" + xss_script)
        return results

