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
	
url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Android+Developer&sc.keyword=Android+Developer&locT=C&locId=1128808&jobType="
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
num_links = 0
for x in formattedURL:
	print (x)
	num_links+=1
print ('There are: ',num_links, ' number of links')

sessions = HTMLSession()
r = sessions.get(formattedURL[4])
print (' this is a sanity check')
print(r.status_code) #sanity check



#xpath declaration
XPATH_NAME = '//*[@class="jobViewJobTitleWrap"]//text()'
XPATH_COMPANY = '//*[@class="strong ib"]//text()'
XPATH_LOC = '//*[@class="subtle ib"]//text()'
XPATH_SALARY = ".//*[@class='salEst']//text()"
XPATH_EVERYTHING = '//*'
XPATH_RATING = '//*[@class="ratingNum"]//text()'
#try except block to catch exceptions (not anymore)

theBiggestList = []
for this_url in formattedURL:	
	response = sessions.get(this_url)
	'''parser = html.fromstring(response.content)

	absolute_url = "https://www.glassdoor.com"
	parser.make_links_absolute(absolute_url)

	bar = parser.xpath(XPATH_EVERYTHING)
	for foo in bar:'''
	print(response)
	tree = html.fromstring(response.content)
	name = tree.xpath(XPATH_NAME)
	print ('This is the job name: ', name)
	company = tree.xpath(XPATH_COMPANY)
	print ('This is the company: ', company)
	rating = tree.xpath(XPATH_RATING)
	print ('This is the overall rating: ', rating)
	salary = tree.xpath(XPATH_SALARY)
	print ('This is the average salary: ', salary)
	location = tree.xpath(XPATH_LOC)
	print ('This is the city and state: ', location)
		
	#########
	#Clean up the dirt
	name_cleaned = ''.join(name).strip('-') if name else None
	company_cleaned = ''.join(company).replace('-','')
	salary_cleaned = ''.join(salary).strip()
	location_cleaned = ''.join(location).strip('-')
	rating_cleaned = ''.join(rating).strip()

	myDict = {
		"Name" : name,
		"Company" : company,
		"Salary" : salary,
		"Location" : location,
		"Rating" : rating
	}
	theBiggestList.append(myDict)	  
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