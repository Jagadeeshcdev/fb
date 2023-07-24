import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def scrape_email_from_facebook(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the elements with CSS selector ".uiScaledImageContainer" and get their attributes
        elements = soup.select(".uiScaledImageContainer")
        emails = []

        for element in elements:
            email = element.get("aria-label")
            if email == "No email address found.":
                continue
            emails.append(email)

        return emails

    except requests.exceptions.RequestException as e:
        st.error(f"Error occurred while scraping the email: {str(e)}")

def main():
    st.title("Facebook Email Scraper")

    # User input: URL
    st.text("Enter the URL of the Facebook page you want to scrape:")
    url = st.text_input("URL", "https://www.facebook.com/kcmplumbingandheating/")

    # Scrape email
    if st.button("Scrape Email"):
        st.text("Scraping email, please wait...")
        emails = scrape_email_from_facebook(url)
        
        if emails:
            st.success("Emails found:")
            for email in emails:
                st.write(email)
        else:
            st.warning("No email address found on the page.")

if __name__ == "__main__":
    main()
