import streamlit as st
import pandas as pd
import subprocess

def scrape_emails():
    st.text("Scraping email, please wait...")
    subprocess.run(["python", "scrape_emails.py"], check=True)

def main():
    st.title("Facebook Email Scraper")

    # Scrape email
    if st.button("Scrape Email"):
        scrape_emails()

        # Load the results into the Streamlit app
        with open('emails.json') as f:
            emails = pd.read_json(f)

        if not emails.empty:
            st.success("Emails found:")
            st.dataframe(emails)
        else:
            st.warning("No email address found on the page.")

if __name__ == "__main__":
    main()
