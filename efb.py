from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_email_from_facebook(url):
    # Set up Chrome options to run headless (without GUI) to avoid opening a visible browser window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load (you may adjust the time if needed)

        # Find the elements with CSS selector ".uiScaledImageContainer" and get their attributes
        elements = driver.find_elements_by_css_selector(".uiScaledImageContainer")
        emails = []

        for element in elements:
            email = element.get_attribute("aria-label")
            if email == "No email address found.":
                continue
            emails.append(email)

        return emails

    except Exception as e:
        print(f"Error occurred while scraping the email: {str(e)}")

    finally:
        driver.quit()

def main():
    url = "https://www.facebook.com/kcmplumbingandheating/"
    emails = scrape_email_from_facebook(url)
    if emails:
        print("Emails found:")
        for email in emails:
            print(email)
    else:
        print("No email address found on the page.")

if __name__ == "__main__":
    main()
