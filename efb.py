import csv
import datetime
import re
import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urljoin
from io import StringIO
import pandas as pd
import time
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor

MAX_WEBSITES = 333

def main():
    st.title("Email Scraper")

    # User input: Websites
    st.text("Enter the URLs of the websites you want to scrape (one URL per line):")
    websites = st.text_area("Websites", "example.com\nexample.org", height=200).strip().split('\n')

    if len(websites) > MAX_WEBSITES:
        st.error(f"Maximum limit exceeded! Please enter up to {MAX_WEBSITES} websites.")
        return

    st.markdown("---")  # Add spacing

    # File upload: CSV
    st.text("Upload a CSV file with websites (one URL per row):")
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])

    if csv_file is not None:
        websites.extend(load_websites_from_csv(csv_file))

    if len(websites) > MAX_WEBSITES:
        st.error(f"Maximum limit exceeded! Please enter up to {MAX_WEBSITES} websites.")
        return

    st.markdown("---")  # Add spacing

    # Scrape emails
    if st.button("Scrape Emails"):
        unique_websites = list(set(websites))  # Remove duplicates
        progress_bar = st.progress(0)
        progress_text = st.empty()
        start_time = time.time()
        results = scrape_emails(unique_websites, progress_bar, progress_text, start_time)
        display_results(results, start_time)

def load_websites_from_csv(file):
    websites = []
    content = file.getvalue().decode("utf-8")
    reader = csv.reader(StringIO(content))
    for row in reader:
        websites.append(row[0])
    return websites

def scrape_emails(websites, progress_bar, progress_text, start_time):
    results = []

    keywords = ['contact', 'contact-us', 'get-in-touch', 'touch', 'about', 'about-us', 'help', 'support']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }

    num_websites = len(websites)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_website, website, keywords, headers) for website in websites]
        for i, future in enumerate(futures):
            website, emails = future.result()
            results.append({'Website': website, 'Emails': emails})
            progress = (i + 1) / num_websites
            progress_bar.progress(progress)
            progress_text.text(f"Progress: {i+1}/{num_websites} websites")

            elapsed_time = time.time() - start_time
            estimated_time = elapsed_time / (i + 1) * (num_websites - (i + 1))
            progress_text.text(f"Progress: {i+1}/{num_websites} websites | Estimated Time: {estimated_time:.2f} seconds")
            time.sleep(0.1)

    return results

def scrape_website(website, keywords, headers):
    try:
        if not website.startswith("http"):
            website = "https://" + website

        response = requests.get(website, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Handle the popup
        handle_popup(soup)

        emails = scrape_email_addresses_from_page(soup)

        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(website, link['href'])
            if any(keyword in absolute_url for keyword in keywords):
                sub_response = requests.get(absolute_url, headers=headers, timeout=30)
                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.content, 'html.parser')

                # Handle the popup in the sub-page
                handle_popup(sub_soup)

                sub_emails = scrape_email_addresses_from_page(sub_soup)
                emails.update(sub_emails)

        return website, emails

    except requests.exceptions.RequestException as e:
        return website, []

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
        r'@[\d.]+$',                    # Exclude email addresses withnumbers (e.g., version numbers)
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

def handle_popup(soup):
    # Find the popup element based on its class name or ID
    popup_element = soup.find("div", class_="x1b0d499 x1d69dk1")  # Replace with the actual class name

    # If the popup element is found, remove it from the soup
    if popup_element:
        popup_element.extract()

# Rest of the code remains the same
# ...

if __name__ == "__main__":
    main()
