#!/bin/bash

# Create a new virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate  # For Linux/macOS
env\Scripts\activate    # For Windows

# Install the required packages
pip install -r requirements.txt
pip install --upgrade streamlit
-m pip install --upgrade pip
pip install requests
pip install bs4
pip install BeautifulSoup
pip install pandas
pip install pd
pip install time
pip install io
pip install StringIO
pip install selenium 
pip install webdriver
pip install selenium.webdriver.chrome.options 
pip install Options
pip install scrapy streamlit requests
pip install scrapy.crawler
pip install CrawlerRunner
