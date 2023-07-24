import scrapy
from scrapy.crawler import CrawlerProcess
import re

class EmailSpider(scrapy.Spider):
    name = 'email_spider'
    start_urls = ['https://www.facebook.com/kcmplumbingandheating/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }

    def parse(self, response):
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

        emails = set()
        for element in response.css('body ::text').getall():
            matches = re.findall(email_regex, element)
            for match in matches:
                if not any(re.match(pattern, match) for pattern in exclude_patterns):
                    emails.add(match)

        return {'emails': list(emails)}

def scrape_facebook_emails():
    process = CrawlerProcess()
    process.crawl(EmailSpider)
    process.start()

if __name__ == '__main__':
    scrape_facebook_emails()
