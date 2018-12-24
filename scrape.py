from time import sleep
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Main_URL = 'http://etsuran.mlit.go.jp/TAKKEN/takkenSearch.do'

options = Options()
options.set_headless(False)

driver = webdriver.Chrome(chrome_options=options)

driver.get(Main_URL)
sleep(1)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")

input_text_name = driver.find_element_by_name('comNameKanaOnly').send_keys("エヌケイハウジング")
sleep(1)
click_selection = driver.find_element_by_xpath('//*[@id="rdoSelectOr"]').click()
sleep(1)
click_number_type = driver.find_element_by_xpath('//*[@id="input"]/div[4]/div[2]/select').click()
sleep(1)
click_type = driver.find_element_by_xpath('//*[@id="input"]/div[4]/div[2]/select/option[3]').click()
sleep(1)
input_text_number = driver.find_element_by_name('licenseNoFrom').send_keys("4314")
sleep(1)
input_text_number = driver.find_element_by_name('licenseNoTo').send_keys("4314")
sleep(1)
click_address_selection = driver.find_element_by_xpath('//*[@id="input"]/div[5]/div[2]/select[2]').click()
sleep(1)
click_address = driver.find_element_by_xpath('//*[@id="input"]/div[5]/div[2]/select[2]/option[48]').click()
sleep(1)
click_button = driver.find_element_by_xpath('//*[@id="input"]/div[6]/div[5]/img').click()
sleep(1)

for company_name in soup.select("#container_cont > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4) > a"):
    print(company_name.get_text())
