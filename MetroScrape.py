# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:16:44 2017

@author: Connor
"""


import pdb, time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    

keyValues = open('keyValues.txt')
keyValues = keyValues.read().split(',')


"""
This data begins in October, 2015, so we want to generate date pairs from then
until whenever now is.
"""

datePairs = []
dateStart = datetime.strptime('10/1/2015', '%m/%d/%Y')
while dateStart <= datetime.now():
    print(dateStart)
    datePairs.append([dateStart.strftime('%m/%d/%Y'), (dateStart+timedelta(days=30)).strftime('%m/%d/%Y')])
    dateStart = dateStart + timedelta(days=31)
    


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : keyValues[0]}
chromeOptions.add_experimental_option("prefs",prefs)

baseURL = r'https://smartrip.wmata.com/Account/AccountLogin.aspx'
driver = webdriver.Chrome(keyValues[1], chrome_options = chromeOptions)

driver.get(baseURL)

"""
User Name Xpath: //*[@id="ctl00_ctl00_MainContent_MainContent_txtUsername"]
Password: //*[@id="ctl00_ctl00_MainContent_MainContent_txtPassword"]
Log In BUtton: //*[@id="ctl00_ctl00_MainContent_MainContent_btnSubmit"]
"""

userName = keyValues[2]
passWord = keyValues[3]

xpathUserName = '//*[@id="ctl00_ctl00_MainContent_MainContent_txtUsername"]'
xpathPW = '//*[@id="ctl00_ctl00_MainContent_MainContent_txtPassword"]'
xpathRange = '//*[@id="ctl00_ctl00_MainContent_MainContent_rbByRange"]'
xpathClickSend = '//*[@id="right_wide"]/div/div/div/div[1]/p[3]/a'

driver.find_element_by_xpath(xpathUserName).send_keys(userName)
driver.find_element_by_xpath(xpathPW).send_keys(passWord)

xpathSubmit = '//*[@id="ctl00_ctl00_MainContent_MainContent_btnSubmit"]'
driver.find_element_by_xpath(xpathSubmit).click()
time.sleep(1)

driver.find_element_by_xpath('//*[@id="left_wide"]/ul/li/a').click()
time.sleep(1)

driver.find_element_by_xpath(xpathClickSend).send_keys(Keys.RETURN)
time.sleep(1)

driver.find_element_by_xpath(xpathRange).click()
time.sleep(1)

xpathBack = '//*[@id="ctl00_ctl00_MainContent_MainContent_btnBack"]'
xpathstartDate = '//*[@id="ctl00_ctl00_MainContent_MainContent_txtStartDate"]'
xpathEndDate = '//*[@id="ctl00_ctl00_MainContent_MainContent_txtEndDate"]'
xpathExport = '//*[@id="ctl00_ctl00_MainContent_MainContent_lnkExport"]'

i = 0
for datePair in datePairs:
    if i > 0:
        driver.find_element_by_xpath(xpathBack).send_keys(Keys.RETURN)

    driver.find_element_by_xpath(xpathstartDate).clear()
    driver.find_element_by_xpath(xpathstartDate).send_keys(datePair[0])
    
    driver.find_element_by_xpath(xpathEndDate).clear()
    driver.find_element_by_xpath(xpathEndDate).send_keys(datePair[1])
    
    time.sleep(1)
    # '//*[@id="ctl00_ctl00_MainContent_MainContent_btnSubmit"]'
    driver.find_element_by_xpath(xpathSubmit).send_keys(Keys.RETURN)

    time.sleep(1)
    try:
        driver.find_element_by_xpath(xpathExport).send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass
    i = 1

time.sleep(1)
driver.find_element_by_xpath('//*[@id="aspnetForm"]/a').send_keys(Keys.RETURN)
time.sleep(1)
driver.quit()




