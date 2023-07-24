import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_email_addresses_from_page(soup):
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
    return email_addresses

def scrape_emails_from_facebook(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        emails = scrape_email_addresses_from_page(soup)

        return emails

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {url}: {e}")
        return []

def main():
    url = "https://www.facebook.com/kcmplumbingandheating/"
    emails = scrape_emails_from_facebook(url)

    if emails:
        print("Scraped email addresses:")
        for email in emails:
            print(email)
    else:
        print("No email addresses found.")

if __name__ == "__main__":
    main()
