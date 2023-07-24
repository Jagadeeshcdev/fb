import streamlit as st
import requests
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class EmailSpider(CrawlSpider):
    name = 'email_spider'
    allowed_domains = ['facebook.com']
    start_urls = ['https://www.facebook.com/kcmplumbingandheating/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        email_addresses = set()
        email_regex = r'[\w.+-]+@[\w-]+\.[\w.-]+'
        exclude_patterns = [
            r'.*\.css',                     # Exclude CSS files
            r'.*\.js',                      # Exclude JavaScript files
            r'.*\.png',                     # Exclude PNG images
            r'.*\.jpg',                     # Exclude JPG/JPEG images
            r'.*\.jpeg',                    # Exclude JPG/JPEG images
            r'.*\.gif',                     # Exclude GIF images
            r'@[\d.]+$',                    # Exclude email addresses with numbers (e.g., version numbers)
            r'react-dom@[\d.]+',             # Exclude react-dom versions
            r'core-js-bundle@[\d.]+',        # Exclude core-js-bundle versions
            r'e9e9f0ab72ed4f4884e049aae0c4c669@sentry.websupport.sk',    # Exclude specific email addresses
            r'search-insights@1\.3\.1',      # Exclude specific email addresses
            r'intersection-observer-polyfill@0\.1\.0',  # Exclude specific email addresses
        ]

        for element in soup.find_all(string=re.compile(email_regex)):
            matches = re.findall(email_regex, element)
            for match in matches:
                if not any(re.match(pattern, match) for pattern in exclude_patterns):
                    email_addresses.add(match)

        return {'emails': list(email_addresses)}

def scrape_with_scrapy():
    from twisted.internet import reactor
    from scrapy.utils.project import get_project_settings

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(EmailSpider)

def main():
    st.title("Facebook Email Scraper")

    # Scrape email
    if st.button("Scrape Email"):
        st.text("Scraping email, please wait...")
        scrape_with_scrapy()

if __name__ == "__main__":
    main()
