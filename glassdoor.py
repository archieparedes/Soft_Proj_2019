from lxml import html, etree
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests_html import HTMLSession



url = ('https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=android+developer&sc.keyword=android+developer&locT=C&locId=1128808&jobType=')

sessions = HTMLSession()
r = sessions.get(url)
print(r.status_code)



#xpath declaration
XPATH_NAME = './/a/text()'
XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
XPATH_LOC = './/span[@class="subtle loc"]/text()'
XPATH_SALARY = './/span[@class="green small"]/text()'
XPATH_EVERYTHING = '//li[@class="jl"]'
XPATH_CITYSTATE = '/html/body/div[3]/div/div/div/div[1]/div/div[2]/section/div/div/article/div/div[1]/div[3]/div[3]/span[2]'
XPATH_RATING = './/div[@class="ratingNum margRtSm"]/div/text()'



#try except block to catch exceptions
try:
		theBiggestList = []
		response = sessions.get(url)
		print(response)
		parser = html.fromstring(response.text)
		
		bar = parser.xpath(XPATH_EVERYTHING)
		for foo in bar:
			foo_name = foo.xpath(XPATH_NAME)
			foo_company = foo.xpath(XPATH_COMPANY)
			foo_money = foo.xpath(XPATH_SALARY)
			foo_citystate = foo.xpath(XPATH_LOC)
			foo_rating = foo.xpath(XPATH_RATING)
			
			
			print(foo_name)
			print(foo_citystate)
			print(foo_rating)
			print(foo_money)
			
			#########
			#Clean up the dirt
			foo_name_cleaned = ''.join(foo_name).strip('-') if foo_name else None
			foo_company_cleaned = ''.join(foo_company).replace('-','')
			foo_money_cleaned = ''.join(foo_money).strip()
			foo_citystate_cleaned = ''.join(foo_citystate).strip('-')

			myDict = {
				"Name" : foo_name_cleaned,
				"Company" : foo_company_cleaned,
				"Salary" : foo_money_cleaned,
				"Location" : foo_citystate_cleaned
			}
			theBiggestList.append(myDict)
		print("works??")
except:
	print("Something went wrong")
	
print(theBiggestList)


keyword = 'test'
place = 'test2'
with open('test-job-results.csv', 'wb') as myfile:
    writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for data in theBiggestList:
        writer.writerow(data.items())