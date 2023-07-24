import requests
from bs4 import BeautifulSoup
import streamlit as st

def close_popup(soup):
    # Identify and close the popup with class "x1b0d499 x1d69dk1" and aria-label "Close"
    popup = soup.find('div', {'class': 'x1b0d499 x1d69dk1', 'aria-label': 'Close'})
    if popup:
        popup.extract()

def scrape_email_from_page(url, css_selector):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        close_popup(soup)  # Close the popup

        email_element = soup.select_one(css_selector)
        email = email_element.text.strip() if email_element else None

        return email

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {url}: {e}")
        return None

def main():
    st.title("Email Scraper")

    url = "https://www.facebook.com/kcmplumbingandheating/"
    css_selector = "#mount_0_0_cv > div > div:nth-child(1) > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x78zum5.xdt5ytf.x1t2pt76 > div > div > div.x6s0dn4.x78zum5.xdt5ytf.x193iq5w > div.x9f619.x193iq5w.x1talbiv.x1swvt13.x1pi30zi.xw7yly9 > div > div.x9f619.x1n2onr6.x1ja2u2z.xeuugli.x1iyjqo2.xs83m0k.x1xmf6yo.x1emribx.x1e56ztr.x1i64zmx.xjl7jj.xnp8db0.x65f84u.x1xzczws > div.x7wzq59 > div > div:nth-child(1) > div > div > div > div > div.xieb3on > div:nth-child(2) > div > ul > div:nth-child(4) > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn > div > div > span"
    email = scrape_email_from_page(url, css_selector)

    if email:
        st.write("Scraped email address:")
        st.write(email)
    else:
        st.write("No email address found.")

if __name__ == "__main__":
    main()
