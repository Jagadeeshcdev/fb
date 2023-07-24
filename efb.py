import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape websites from a table
def scrape_websites(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the websites
    table = soup.select_one('table#sites_tbl')
    if table:
        # Find all rows in the table
        rows = table.select('td.row_name > a')
        websites = []
        for row in rows:
            # Find the website URL in each row
            website_url = row['href']
            websites.append(website_url)

        return websites

    return []

# Function to get the next page URL
def get_next_page_url(url, page_number):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the next page button and extract the URL
    next_button = soup.select_one(f'div#tabs-1 div.padding17.sites_tbl_paging > div > a:nth-child({page_number})')
    if next_button:
        return next_button['href']

    return None

# Create the Streamlit app
st.title("Website Scraping")
main_url = st.text_input("Enter the main page URL:")
if st.button("Scrape Websites"):
    # Initialize progress bar and elapsed time
    progress_bar = st.progress(0)
    start_time = time.time()

    scraped_websites = []
    page_count = 1
    page_url = main_url
    while page_url:
        # Scrape websites from current page
        new_websites = scrape_websites(page_url)
        scraped_websites.extend(new_websites)

        # Update progress bar
        progress = len(scraped_websites) / 100
        progress_bar.progress(progress)

        # Get the next page URL
        page_count += 1
        next_page_url = get_next_page_url(main_url, page_count)
        if next_page_url:
            page_url = main_url + next_page_url
            st.write("Scraping page", page_count, ":", page_url)
        else:
            page_url = None

    # Display scraped websites in a table
    df = pd.DataFrame({'Website URLs': scraped_websites})
    if not df.empty:
        st.write(df)
        # Download scraped websites as CSV
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="scraped_websites.csv")
    else:
        st.write("No websites found.")

    # Display elapsed time
    elapsed_time = round(time.time() - start_time, 2)
    st.write("Elapsed Time:", elapsed_time, "seconds")
