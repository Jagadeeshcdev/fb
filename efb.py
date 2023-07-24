import streamlit as st
import pandas as pd

def main():
    st.title("Facebook Email Scraper")

    # Load the results from the JSON file
    try:
        with open('emails.json') as f:
            emails = pd.read_json(f)
    except FileNotFoundError:
        emails = pd.DataFrame()

    # Display email addresses
    if not emails.empty:
        st.success("Emails found:")
        st.dataframe(emails)
    else:
        st.warning("No email address found on the page.")

if __name__ == "__main__":
    main()
