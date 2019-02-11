
from time import sleep
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm

import csv

import html5lib

import re


Main_url = "http://www.uema-housing.com/areac1_uh/"

Main_title = []



options = Options()
options.set_headless(True)

driver = webdriver.Chrome(chrome_options=options)

driver.get(Main_url)
sleep(1)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")

click_all = driver.find_element_by_xpath("//*[@id='searchForm']/div[2]/div/span/label/input")
sleep(1)

click_search = driver.find_element_by_xpath("//*[@id='searchForm']/p/a/img")
sleep(1)

target_title = r"<p class='bknttl'></p>"
matched_list = re.finditer(target_title, str(soup))

for match in matched_list:
    print(match)

    if match:
        title = match.groups()[0].replace(' ', '').replace("%20", "")
        Main_title.append(title)
        print(Main_title)

    break
