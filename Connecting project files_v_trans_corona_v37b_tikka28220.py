# Scrapping many webpages with selenium, BeautifulSoup and parraller driving. Works best in cluster computers,
# but perfectly ok for PCs and smaller data. Pauli Tikka et al. 5.3.2020 

#Some preliminary infos (maybe too many..):

#Pandas manipulations:
#https://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.html
#https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/
#https://note.nkmk.me/en/python-pandas-dataframe-rename/
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html

#List and string manipulations:
#https://www.pythonforbeginners.com/basics/string-manipulation-in-python
#https://developers.google.com/edu/python/regular-expressions
#https://www.geeksforgeeks.org/find-all-the-numbers-in-a-string-using-regular-expression-in-python/
#https://stackoverflow.com/questions/949098/python-split-a-list-based-on-a-condition
#https://www.geeksforgeeks.org/python-merge-list-elements/      
#https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
#https://realpython.com/python-string-split-concatenate-join/
#https://www.pythonforbeginners.com/concatenation/string-concatenation-and-formatting-in-python

#General about Selenium, Beautifulsoup, and Scrapy web scrapping with python:
#https://medium.com/analytics-vidhya/scrapy-vs-selenium-vs-beautiful-soup-for-web-scraping-24008b6c87b8
#https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python
#https://docs.python.org/3/library/urllib.request.html
#https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
#https://automatetheboringstuff.com/chapter11/

#Specific about web scrapping
#https://jkotests.wordpress.com/2013/07/10/changing-an-elements-attribute-value/
#https://selenium-python.readthedocs.io/locating-elements.html
#https://www.w3schools.com/jsref/met_document_getelementbyid.asp
#https://www.w3schools.com/js/js_htmldom_elements.asp
#https://www.w3schools.com/jsref/met_form_reset.asp
#https://stackoverflow.com/questions/41682993/replace-placeholder-text-on-a-webpage-using-python-and-selenium
#https://stackoverflow.com/questions/10596417/is-there-a-way-to-get-element-by-xpath-using-javascript-in-selenium-webdriver
#https://stackoverflow.com/questions/18557275/how-to-locate-and-insert-a-value-in-a-text-box-input-using-python-selenium
#https://stackoverflow.com/questions/1629053/typing-enter-return-key-using-python-and-selenium
#https://stackoverflow.com/questions/56205245/running-execute-script-with-variable-inside-in-python-via-selenium/56213477

#Making dates or values:
#https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python
#https://stackoverflow.com/questions/18265935/python-create-list-with-numbers-between-2-values

#Troubleshooting:
#https://stackoverflow.com/questions/41466431/pip-install-json-fails-on-ubuntu
#https://stackoverflow.com/questions/13553497/document-getelementbyid-value-doesnt-set-the-value
#https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path

#%%Importing pagckages
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd #for importing files
import numpy as np  #for calculations, array manipulations, and fun :)
import matplotlib.pyplot as plt #for scientifical plots
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import datetime
import time
from selenium import webdriver  # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed

#%% All urls, once you have it do not do it many times, it lasts around 15 min..
all_urls = []
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)

driver.get('http://103.247.238.92/dghseams/attend/professional_category_wise.php')
divs = driver.find_elements_by_class_name('link')

divisions_urls = [{'div_name':div.get_attribute('text'), 'div_url':div.get_attribute('href')} for div in divs]

for div_url in divisions_urls:
    driver.get(div_url['div_url'])
    
    dists = driver.find_elements_by_class_name('link')
    
    districts_urls = [{'dist_name':dist.get_attribute('text'), 'dist_url':dist.get_attribute('href')} for dist in dists]
    
    
    for dist_url in districts_urls:
        driver.get(dist_url['dist_url'])

        upzs = driver.find_elements_by_class_name('link')
        
        upazilas_urls = [{'div_name':div_url['div_name'],
                          'dist_name':dist_url['dist_name'],
                          'upz_name':upz.get_attribute('text'), 
                          'upz_url':upz.get_attribute('href')} for upz in upzs]

        all_urls.append(upazilas_urls)
#%%list of urls
flattened_list = [y for x in all_urls for y in x]    
df = pd.DataFrame(flattened_list, columns = ['div_name', 'dist_name','upz_name', 'upz_url'])
#%%test df
df
#%%The dates, this should be fast:
start = datetime.datetime.strptime("2019-11-26", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-02-29", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
dates=[]
for date in date_generated:
    dates.append(date.strftime("%Y-%m-%d"))
#%% 'dated urls''
dated_urls = []
for i in range(len(df)):
    for date in dates:

        breaked_url = df['upz_url'][i].split("cdate")[0]
        date_url = 'cdate={}&cdate2={}'.format(date,date) 
        new_url = breaked_url + str(date_url)
        
        new_row = {"division":df['div_name'][i],"district":df['dist_name'][i],
                   "upazila":df['upz_name'][i],"date":date,"url":new_url}
        dated_urls.append(new_row)

#         print(dated_urls)
#%%dated urls in panda and csv:
dated_df = pd.DataFrame(dated_urls)
dated_df.to_csv("dated_urls")     
#%%in the future, you just do this:
dated_df = pd.read_csv("dated_urls")
#dated_df  

#%%The parallisation (Thank you Ali for the code):
def parse_req(url,dated_row):
    
    
    old_names = ['Organization', 'Orgs. with functioning attendance system',
       'Orgs. sending data', 'No. of Posts', 'No. of Posts.1',
       'No. of Posts.2', 'Vacancy(%)', 'No. of staffs', 'No. of staffs.1',
       'No. of staffs.2', 'Attendance (%)']

    new_names = ['Organization', 'Orgs. with functioning attendance system',
       'Orgs. sending data', 'Sanctioned', 'Filled', 'Vacant', 'Vacancy(%)',
       'Rgd. in attendance system', 'Present*', 'Absent', 'Attendance (%)']
    
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    soup1 = pd.read_html(str(soup),header=0)
    soup2 = pd.DataFrame(soup1[0])
    
    soup2.rename(columns=dict(zip(old_names, new_names)), inplace=True)
    soup2.drop([0, 2], inplace=True)

    a = pd.DataFrame(dated_row).transpose()
    a.reset_index(drop=True, inplace=True)

    b = soup2
    b.reset_index(drop=True, inplace=True)

    row = pd.concat([a, b], axis=1)  
#         print(row)
    
    
    return row
#%%Driving the whole thing for doctors:
from concurrent.futures import as_completed, ProcessPoolExecutor
import time
import numpy as np
import winprocess
from bs4 import BeautifulSoup
import alpine
#%%

doctors_df = pd.DataFrame()
start = time.time()

with ProcessPoolExecutor(max_workers=20) as executor:
    futures = set()
    for index, dated_row in dated_df.iterrows():
        url = dated_row["url"]
        future = winprocess.submit(executor, parse_req, url,dated_row)
        futures.add(future)

    for future in as_completed(futures):
        
        doctors_df = pd.concat([doctors_df, future.result()], axis=0)
        
end = time.time()
print("Time Taken: {:.6f}s".format(end-start))   
#%%saving the data for all doctors
doctors_df.reset_index(drop=True, inplace=True)
doctors_df.drop(columns=['Unnamed: 0'], inplace=True)
doctors_df
#%%
doctors_df.to_csv("all_doctors.csv") 

#%%For the other groups:
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)

#%%The parse command has similarities:
def parse_req_all(url,dated_row):
    
    old_names = ['Organization', 'Orgs. with functioning attendance system',
       'Orgs. sending data', 'No. of Posts', 'No. of Posts.1',
       'No. of Posts.2', 'Vacancy(%)', 'No. of staffs', 'No. of staffs.1',
       'No. of staffs.2', 'Attendance (%)']

    new_names = ['Organization', 'Orgs. with functioning attendance system',
       'Orgs. sending data', 'Sanctioned', 'Filled', 'Vacant', 'Vacancy(%)',
       'Rgd. in attendance system', 'Present*', 'Absent', 'Attendance (%)']
    
    
    driver.get(url);
    
    rows = pd.DataFrame()
    for prof_cat in ["Doctor", "Nurse","Others"]:
    
        search_box0 = driver.find_element_by_name('prof_category')
        search_box0.send_keys(Keys.CONTROL, 'a')
        search_box0.send_keys(Keys.BACKSPACE)
        search_box0.send_keys(prof_cat)
        print(prof_cat)
        
        search_boxn=driver.find_elements_by_xpath("//input[@name='submit' and @value='show report']")[0]
        search_boxn.click()
    
    
        soup = BeautifulSoup(driver.page_source, 'lxml')
        soup1 = pd.read_html(str(soup),header=0)
        soup2 = pd.DataFrame(soup1[0])

        soup2.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        soup2.drop([0, 2], inplace=True)

        a = pd.DataFrame(dated_row).transpose()
        a.reset_index(drop=True, inplace=True)

        b = soup2
        b.reset_index(drop=True, inplace=True)

        row = pd.concat([a, b], axis=1) 
        row["professional category"]= prof_cat
        rows = pd.concat([rows,row], axis=0)
        print(rows)

    
    return rows
#%%
from concurrent.futures import as_completed, ProcessPoolExecutor
import time
import numpy as np
import winprocess
from bs4 import BeautifulSoup


all_df = pd.DataFrame()
start = time.time()

with ProcessPoolExecutor(max_workers=20) as executor:
    futures = set()
    for index, dated_row in dated_df[:3].iterrows():
        url = dated_row["url"]
        future = winprocess.submit(executor, parse_req_all, url,dated_row)
        futures.add(future)

    for future in as_completed(futures):
        
        all_df = pd.concat([all_df, future.result()], axis=0)
        
end = time.time()
print("Time Taken: {:.6f}s".format(end-start))
#%%
all_df.reset_index(drop=True, inplace=True)
all_df.drop(columns=['Unnamed: 0'], inplace=True)
all_df
#%%saving the data for all docros nurses and other group
all_df.to_csv("all_dfs.csv")    
