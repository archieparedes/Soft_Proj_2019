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

jobDescriptionURL = []
secondListURL = []
formattedURL = []
theBiggestList = []
absoluteURL = 'http://glassdoor.com'

#change the user agent so that we dont get a 403 error
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	
#These are the google credentials and links for connecting to the sheets API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# #name of sheet in my google sheets
sheet = client.open('glassdoor Jobs')
	
url = "https://www.glassdoor.com/Job/chicago-android-developer-jobs-SRCH_IL.0,7_IC1128808_KO8,25.htm"
theURL = "https://www.glassdoor.com/Job/chicago-android-developer-jobs-SRCH_IL.0,7_IC1128808_KO8,25_IP"
urlList = []


print (theURL)
count = 2
for x in range (0,5): #here brute force many pages of glassdoor using the list append function
	urlList.append((theURL + str(count) + '.htm')) #there should be a better way of doing this, but I don't know right now
	count +=1 #you can print out the list of urls if it looks like its not getting them properly
print('the number of unique urls is: ' + str(len(urlList))) #check to make sure that there is a reasonable amount of links
print (urlList)
	
headers = {'User-Agent':user_agent,} #apply the user agent here

def masterFunction(): #make the soup creation a function so that we can use the list of URLs instead of a hard coded url
	for urlPoint in urlList:
		request = urllib.request.Request(urlPoint,None,headers)
		response = urllib.request.urlopen(request)
		data = response.read() #this is the raw html in case it's needed
		soup = BeautifulSoup(data, "lxml")
		soup.prettify()
		for soupHTML in soup.findAll('a', href = re.compile('/partner+')):
			jobDescriptionURL.append(soupHTML['href'])
			print(jobDescriptionURL)

masterFunction()

def cleanFunction():
	for appendStep in jobDescriptionURL:
		secondListURL.append(absoluteURL + appendStep)
	for cleaned in secondListURL:
		stuff = cleaned.strip()
		formattedURL.append(stuff)
		print('\n')
		print(formattedURL)
		
cleanFunction()

for x in formattedURL:
	print (x)
	count +=1
print('There are: ',count, ' total URLs')	
print('\n\n\n\n\n')

XPATH_NAME = '//*[@class="jobViewJobTitleWrap"]//text()'
XPATH_COMPANY = '//*[@class="strong ib"]//text()'
XPATH_LOC = '//*[@class="subtle ib"]//text()'
XPATH_SALARY = ".//*[@class='salEst']//text()"
XPATH_EVERYTHING = '//*'
XPATH_RATING = '//*[@class="ratingNum"]//text()'

sessions = HTMLSession()

for this_url in formattedURL:	
	response = sessions.get(this_url)
	print(response)
	tree = html.fromstring(response.content)
	name = tree.xpath(XPATH_NAME)
	company = tree.xpath(XPATH_COMPANY)
	rating = tree.xpath(XPATH_RATING)
	salary = tree.xpath(XPATH_SALARY)
	location = tree.xpath(XPATH_LOC)
	
	'''name_clean = name.split()
	company_clean = company.split()
	rating_clean = rating.split()
	salary_clean = salary.split()
	location_clean = location.split()'''
	
	#print(name, '\n',company, '\n',rating, '\n',salary, '\n',location, '\n')
	myDict = {
		"Name" : name,
		"Company" : company,
		"Salary" : salary,
		"Location" : location,
		"Rating" : rating
	}
	theBiggestList.append(myDict)	
	
with open('testJobResults.csv', 'wb') as myfile:
    fieldnames = ['Name', 'Company', 'Salary', 'Location', 'Rating']
    writer = csv.DictWriter(myfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for data in theBiggestList:
        writer.writerow(data)
csv = open('testJobResults.csv', 'r')
finalcsv = csv.read().encode(encoding = 'UTF-8', errors='strict')
client.import_csv(sheet.id, finalcsv)