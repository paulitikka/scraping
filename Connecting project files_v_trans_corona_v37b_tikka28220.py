# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 11:16:40 2020

@author: Pauli Tikka
"""
# Task 2.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 2019 and January 14 2020, and use also google searches: 

#Date	(1)
#Facility name (2 etc.)	
#Division	
#District	
#Upazila	?
#Orgs. with functioning attendance system	
#Orgs. sending data	
#Sanctioned posts	
#Filled posts	
#Vacant posts	
#Rgd. in attendance system	
#Present 	
#Absent (..until 13)

#Info from Pascal:
#It would be important to have this for each day 
#(i.e., the start and end date needs to be the same;) 
#starting on January 1st 2016 up to today (and updatable per day)
#%%
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd #for importing files
import numpy as np  #for calculations, array manipulations, and fun :)
import matplotlib.pyplot as plt #for scientifical plots
import os
#Some preliminary infos:
# https://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.html
#https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://www.geeksforgeeks.org/find-all-the-numbers-in-a-string-using-regular-expression-in-python/
#https://stackoverflow.com/questions/949098/python-split-a-list-based-on-a-condition
#https://www.geeksforgeeks.org/python-merge-list-elements/      
#%%
#ONE DAY CODE BELOW
#With the belwo code, I can see the Division, and the names of the divisions
# e.g. Barisal and Chattogram
#First you need two auxillary functions:
#% 1) For e.g. dividing a matrix:
#https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(l, n):      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n]  
#% 2) For selecting the right elements from the preliminary download, e.g. with 
#regular experssions:
def sel_loop(ll):
    at=ll
    iii=[]   
    for i in range(len(at)):
        iii.append(str(at[i]))   
    iv=[]
    iv=pd.DataFrame(iii)
    vi=[]
    for i in range(len(iv[0])):
        vi.append(re.split('<|>', iv[0][i]))
#%Real:
    xi=[]
    xii=[]
    for i in range(len(vi)):
        if len(vi[i])==9:
            xi.append(vi[i][4])
        if len(vi[i])==5:
            xii.append(vi[i][2])
        if vi[i][2]=='Total':
            break
    xii.pop(len(xii)-1)
    # How many elements each 
    # list should have 
    n = 11
    x = list(divide_chunks(xii, n)) 
    #%Here is the start:
    #https://note.nkmk.me/en/python-pandas-dataframe-rename/
    df = pd.DataFrame(x,index=xi)
    return(df)
#%%In order to make the main function (tot) look less heavy, 
# you can insert some of the static variables outside the function    
urln_ale='http://103.247.238.92/dghseams/attend/index.php'
soupn=[]
responsen=[]
a_tagn=[]
a_tagn1=[]
a_tagn2=[]
responsen = requests.get(urln_ale)
soupn = BeautifulSoup(responsen.text, 'html.parser')
#a_tagn.append(soupn.findAll('td')) #ok
a_tagn1.append(soupn.findAll('a')) #ok
#a_tagn2.append(soupn.findAll('th')) #ok
#The you can do this for ALL (8) DIVISIONS:
#%%
def tot(n=8):    
    #% From the previous, lest test to find and open Barrisal link:
    #%Let's test first with hospitals (district):
    #DISTRICTS of ONE DIVISION (BARISAL), e.g.:
    #%
    result=[]
    for i in range(6,6+n):  
        #check that your range is ok; the region name tags in the 'a_tagn1 start from 6
        #%
        utot2=urln_ale+a_tagn1[0][i]['href'] #THIS IT THE BIG LOOP in this case! :)
        soupn=[]
        responsen=[]
        a_tagn3=[]
        responsen=requests.get(utot2)
        soupn=BeautifulSoup(responsen.text, 'html.parser')
        a_tagn3=soupn.findAll('a') #ok
        e=[]
        #%
        for i in range(len(a_tagn3)-6):
            if a_tagn3[6+i]['href'].find('hospital') > -1:
                e.append(a_tagn3[6+i]['href']) 
        utot3a=[]
        for i in range(len(e)):
            utot3a.append(urln_ale+e[i]) 
                        #%
        soupn=[]
        responsen=[]
        a_tagn4=[]
        a_tagn4t=[]
        for i in range(len(utot3a)):
            responsen.append(requests.get(utot3a[i]))
            #%
            soupn.append(BeautifulSoup(responsen[i].text, 'html.parser'))
            #%
        for i in range(len(soupn)):
            a_tagn4.append(soupn[i].findAll('a')) #ok
            a_tagn4t.append(soupn[i].findAll('td'))
        df=[]
        for i in range(len(a_tagn4t)):    
            df.append(sel_loop(ll=a_tagn4t[i]))  
            #%
        #    https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        result.append(pd.concat(df))
        #%
    return utot3a, pd.concat(result)
#%%The saving one day to file:
utot3a, result_all=tot(n=8)
#%
#result_all.to_csv('C:/python/division_all hospitals_one_day_tikka17220.csv',index=True,header=False)

#ONE DAY OK HERE LINE
#%% X DAYS CODE BELOW:

#%Now I need the list of day values:
#% This is how I applied the exsiting code for making a day list:
#https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python
import datetime
start = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d") #90d starts: 2019-11-26
end = datetime.datetime.strptime("2020-02-27", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
d=[]
for date in date_generated:
    d.append(date.strftime("%Y-%m-%d"))
#%%Some info for using selenium and we requests:    
#https://docs.python.org/3/library/urllib.request.html
#https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path
#https://stackoverflow.com/questions/41682993/replace-placeholder-text-on-a-webpage-using-python-and-selenium
#https://selenium-python.readthedocs.io/locating-elements.html
#https://stackoverflow.com/questions/18557275/how-to-locate-and-insert-a-value-in-a-text-box-input-using-python-selenium
import time
from selenium import webdriver  # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.common.exceptions import TimeoutException

#%% For making this daywise, one needs to have a codde with the day (d[0]):
#https://stackoverflow.com/questions/1629053/typing-enter-return-key-using-python-and-selenium
#def driveri(str='http://103.247.238.92/dghseams/attend/professional_category_wise.php'):
##    https://sqa.stackexchange.com/questions/2609/running-webdriver-without-opening-actual-browser-window
##    This option is for not opening the window physically, which is needed, since you need to open many:
#    option = webdriver.ChromeOptions()
#    option.add_argument('headless')
#    driver = webdriver.Chrome('C:/Users/Pauli/Downloads/chromedriver.exe', options=option)  # Optional argument, if not specified will search path.
#    driver.get(str);
#    search_box = driver.find_element_by_name('cdate')
#    
#    search_box.send_keys(Keys.CONTROL, 'a')
#    search_box.send_keys(Keys.BACKSPACE)
#    search_box.send_keys(d[0])
#    
#    search_box2 = driver.find_element_by_name('cdate2')
#    search_box2.send_keys(Keys.CONTROL, 'a')
#    search_box2.send_keys(Keys.BACKSPACE)
#    search_box2.send_keys(d[0])
#    
#    search_boxn=driver.find_elements_by_xpath("//input[@name='submit' and @value='show report']")[0]
#    search_boxn.click()
#    #Hah! Worked!
#    #%The below works as well.. this should do the trick:
#    soup=BeautifulSoup(driver.page_source) 
#    return soup
#%%
#test=driveri(str='http://103.247.238.92/dghseams/attend/professional_category_wise.php')  
#%%Now the real thing:
def driverix(ut4, x=2):
#    https://sqa.stackexchange.com/questions/2609/running-webdriver-without-opening-actual-browser-window
#    This option is for not opening the window physically, which is needed, since you need to open many:
#    https://stackoverflow.com/questions/18265935/python-create-list-with-numbers-between-2-values
    s=[]
    from json import dumps
    for i in range(0,x): #Note the range, you have only 1 day data on your scope now...
        try:
            options = webdriver.ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('headless')
            driver = webdriver.Chrome('C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
            driver.set_page_load_timeout(page_load_timeout=500)
            #The above option 'prefs' images do not make it faster.. or then it just did not do it..
    #     # Optional argument, if not specified will search path.
            driver.get(ut4);       
    #https://stackoverflow.com/questions/56205245/running-execute-script-with-variable-inside-in-python-via-selenium/56213477
    #https://www.w3schools.com/js/js_htmldom_elements.asp
    #https://www.w3schools.com/jsref/met_document_getelementbyid.asp
    #https://stackoverflow.com/questions/10596417/is-there-a-way-to-get-element-by-xpath-using-javascript-in-selenium-webdriver
    #https://stackoverflow.com/questions/13553497/document-getelementbyid-value-doesnt-set-the-value
    #https://jkotests.wordpress.com/2013/07/10/changing-an-elements-attribute-value/
    #https://realpython.com/python-string-split-concatenate-join/
            script='document.getElementById("f_date1").value ='
            scripta='document.getElementById("f_date2").value ='
            script1=script+dumps(d[i]) 
            script2=scripta+dumps(d[i]) 
            #Note that the elements are better to add here
            #https://stackoverflow.com/questions/41466431/pip-install-json-fails-on-ubuntu
            #https://www.pythonforbeginners.com/concatenation/string-concatenation-and-formatting-in-python
            #https://www.w3schools.com/jsref/met_form_reset.asp
            driver.execute_script(script1)
            driver.execute_script(script2)
            
            userName = driver.find_element_by_xpath("//input[@name='submit' and @value='show report']")
            driver.execute_script("arguments[0].click();", userName)
    
    #        driver.find_elements_by_xpath("//input[@name='submit' and @value='show report']")[0].click()
            ##%The below works as well.. this should do the trick:
            s.append(BeautifulSoup(driver.page_source)) 
    #        https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python
            driver.quit()
        except TimeoutException:
            pass
        except ValueError:
   # handle ValueError exception
           pass
        except (TypeError, ZeroDivisionError):
   # handle multiple exceptions
   # TypeError and ZeroDivisionError
           pass
        except:           
   # handle all other exceptions
           pass
#        a_t.append(s[i].findAll('a')) #ok
#        https://automatetheboringstuff.com/chapter11/
#        https://medium.com/analytics-vidhya/scrapy-vs-selenium-vs-beautiful-soup-for-web-scraping-24008b6c87b8
    return s  
#%%Now I need a new 'tot' function:
#%Let's start with the auxialiry function:
# Fixing cell loop for toti, big days:

def sel_loopi(ll):
    #%
    at=ll
    iii=[]   
    for i in range(len(at)):
        iii.append(str(at[i]))   
    iv=[]
    iv=pd.DataFrame(iii)
    vi=[]
    for i in range(len(iv[0])):
        vi.append(re.split('<|>', iv[0][i]))
#%Real:
    xi=[]
    xii=[]
    for i in range(len(vi)):
        if len(vi[i])==9:
            xi.append(vi[i][4])
        if len(vi[i])==5:
            xii.append(vi[i][2])
        if vi[i][2]=='Total':
            break
    xii.pop(len(xii)-1)
    # How many elements each 
    #% list should have 
    n = 13 #check this, it may be different in with nurses and doctors etc.
    x = list(divide_chunks(xii, n)) 
    #%Here is the start:
    #https://note.nkmk.me/en/python-pandas-dataframe-rename/
    df = pd.DataFrame(x,index=xi)
    return(df)
#%% Check the amount of days you want (now it is just 2..)   
ok=driverix(str='http://103.247.238.92/dghseams/attend/professional_category_wise.php', x=1)#ok, works..
a_tagn=[]
a_tagn1=[]
a_tagn2=[] 
for i in range(len(ok)): 
    a_tagn.append(ok[i].findAll('td')) #ok
    a_tagn1.append(ok[i].findAll('a')) #ok
    a_tagn2.append(ok[i].findAll('th')) #ok
#%% This below should be for all days:
def toti(utot4a,x=90):    

    #%% Need to do the driveris again..:
    ut4=pd.DataFrame(ut4a[21:31]).reset_index()
    ut4=ut4[0]
    #%%
    soupne=[]
    for i in range(len(utot4a)):
        soupne.append(driverix(utot4a[i], x=57)) 
        #It is not clear that this is ok.., e.g. does the date comes twice?
        #The speed is around 13-15s per page, e.g. it took 14 min with 65 pages
        #Why 1.2.2020 had 95 entries, where as 17.2. only 65?
    #%If the previous is ok (24.2.2020), then the below must change [0] -> something else, 2?
        #Yes, since now we really want two to (n) days..
        #%%
    a_tagn4=[]
    a_tagn4t=[]
    for i in range(len(soupn)):
        for j in range(len(soupn[i])):
            a_tagn4.append(soupn[i][j].findAll('a')) #ok
            a_tagn4t.append(soupn[i][j].findAll('td'))
    #%%This could or should be ok.. (25.2.2020)   
    df=[]
    #%
    for i in range(len(a_tagn4t)):    
        df.append(sel_loopi(ll=a_tagn4t[i]))  #sel_loop not ok this tipme..
        #check sel_loopi..
    #    https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    #%%
    result=[]
    result=pd.concat(df)
#%%%
result.to_csv('C:/python/division_all hospitals_n_days_tikka28220.csv',index=True,header=False)
#%
#    return pd.concat(result)
#%%The saving one day to file:
result=toti(utot4a,x=90)
#https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python
#result.to_csv('C:/python/division_all hospitals_one_specific_day_tikka01012020.csv',index=True,header=False)
#%%The below maybe needed later on converged with other methods:
#https://www.pythonforbeginners.com/basics/string-manipulation-in-python
#%%The links to all divisions (with a single day):
urln_ale='http://103.247.238.92/dghseams/attend/professional_category_wise.php'
soupn=[]
responsen=[]
a_tagn=[]
a_tagn1=[]
a_tagn2=[]
responsen = requests.get(urln_ale)
soupn = BeautifulSoup(responsen.text, 'html.parser')
a_tagn1.append(soupn.findAll('a')) #ok    
#%%
#for i in range(6,):  
    #check that your range is ok; the region name tags in the 'a_tagn1 start from 6
    #%
    #%%
utot2=[]
for i in range(4,12):
    utot2.append(urln_ale+a_tagn1[0][i]['href']) #THIS IT THE BIG LOOP in this case! :)
soupn=[]
responsen=[]
a_tagn3=[]
#%%
for i in range(len(utot2)):
    responsen.append(requests.get(utot2[i]))
    soupn.append(BeautifulSoup(responsen[i].text, 'html.parser'))
    a_tagn3.append(soupn[i].findAll('a')) #ok
    #%%
e=[]
#%
for i in range(len(a_tagn3)):
    for j in range(4, len(a_tagn3[i])):
        e.append(a_tagn3[i][j]['href']) #here is the list of 65 places
#%%        
utot3a=[]
for i in range(len(e)):
    utot3a.append(urln_ale+e[i])     

#%%
soupn=[]
responsen=[]
a_tagn4=[]
a_tagn4t=[]
for i in range(len(utot3a)):
    responsen.append(requests.get(utot3a[i]))
    soupn.append(BeautifulSoup(responsen[i].text, 'html.parser'))
    #%
for i in range(len(soupn)):
    a_tagn4.append(soupn[i].findAll('a')) #ok
#    a_tagn4t.append(soupn[i].findAll('td'))
#%%
e2=[]
for i in range(len(a_tagn4)):
    for j in range(4, len(a_tagn4[i])):
        e2.append(a_tagn4[i][j]['href']) #here is the list of all ~500 places  
#%%
utot4a=[]
for i in range(len(e2)):
    utot4a.append(urln_ale+e2[i])  
    #%%
#    Trying to save utot4a..:
ut4a=pd.DataFrame(utot4a)
#%%
ut4a.to_csv('C:/python/the sites of hospitas.csv',index=False,header=False)     
#%%
#https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/
ut4a = pd.read_csv("the sites of hospitas.csv",header=None)   
#%These are the links:
utot4a=[]
for i in range(len(ut4a)):
    utot4a.append(ut4a[0][i])


        #%%

