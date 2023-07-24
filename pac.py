import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
from selenium import webdriver
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
