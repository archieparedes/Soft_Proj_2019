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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from getLinks import get_all_job_links
import urllib.request

#These are the google credentials and links for connecting to the sheets API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# #name of sheet in my google sheets
sheet = client.open('glassdoor Jobs')

jobDescriptionURL = []
secondListURL = []
formattedURL = []
absoluteURL = 'http://glassdoor.com'

#change the user agent so that we dont get a 403 error
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	
url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=Android&sc.keyword=Android+Developer&locT=C&locId=1128808&jobType="
headers = {'User-Agent':user_agent,} #apply the user agent here

request = urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(request)
data = response.read() #this is the raw html in case it's needed
soup = BeautifulSoup(data, "lxml")
soup.prettify()

def get_all_job_links(): #condense all of the link creation here
	for foo in soup.findAll('a', href = re.compile('/partner+')):
		jobDescriptionURL.append(foo['href'])
	for foo in jobDescriptionURL:
		secondListURL.append(absoluteURL + foo)
	for foo in secondListURL:
		stuff = foo.strip()
		formattedURL.append(stuff)
	
get_all_job_links()


sessions = HTMLSession()
r = sessions.get(formattedURL[4])
print (' this is a sanity check')
print(r.status_code) #sanity check



#xpath declaration
XPATH_NAME = '//*[@class="jobViewJobTitleWrap"]'
XPATH_COMPANY = '//*[@class="strong ib"]'
XPATH_LOC = '//*[@class="subtle ib"]'
XPATH_SALARY = ".//*[@class='salEst']"
XPATH_EVERYTHING = '//*'
XPATH_RATING = '//*[@class="empStatsBody"]'

#try except block to catch exceptions
try:
	for my_urls in formattedURL:
		theBiggestList = []
		response = sessions.get(my_urls)
		print(response)
		parser = html.fromstring(response.content)

		absolute_url = "https://www.glassdoor.com"
		parser.make_links_absolute(absolute_url)

		bar = parser.xpath(XPATH_EVERYTHING)
		for foo in bar:
			foo_name = foo.xpath(XPATH_NAME)
			foo_company = foo.xpath(XPATH_COMPANY)
			foo_money = foo.xpath(XPATH_SALARY)
			foo_citystate = foo.xpath(XPATH_LOC)
			foo_rating = foo.xpath(XPATH_RATING)
			
			
			print(foo_name)
			print(foo_company)
			print(foo_citystate)
			print(foo_rating)
			print(foo_money)
			
			#########
			#Clean up the dirt
			foo_name_cleaned = ''.join(foo_name).strip('-') if foo_name else None
			foo_company_cleaned = ''.join(foo_company).replace('-','')
			
			foo_money_cleaned = ''.join(foo_money).strip()
			foo_citystate_cleaned = ''.join(foo_citystate).strip('-')
			foo_rating_cleaned = ''.join(foo_rating).strip()

			myDict = {
				"Name" : foo_name_cleaned,
				"Company" : foo_company_cleaned,
				"Salary" : foo_money_cleaned,
				"Location" : foo_citystate_cleaned,
				"Rating" : foo_rating_cleaned
			}
			theBiggestList.append(myDict)
	print("works??")
except:
	print("Something went wrong")
	  
print(theBiggestList)


keyword = 'test'
place = 'test2'
with open('testJobResults.csv', 'wb') as myfile:
    fieldnames = ['Name', 'Company', 'Salary', 'Location', 'Rating']
    writer = csv.DictWriter(myfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for data in theBiggestList:
        writer.writerow(data)
csv = open('testJobResults.csv', 'r')
finalcsv = csv.read().encode(encoding = 'UTF-8', errors='strict')
client.import_csv(sheet.id, finalcsv)
