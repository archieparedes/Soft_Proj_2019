from bs4 import BeautifulSoup
import urllib.request
from requests_html import HTMLSession
import re
import requests
from lxml import html

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


count = 0

for x in formattedURL:
	print (x)
	count +=1
print('There are: ',count, ' total URLs')	
print('\n\n\n\n\n')

sessions = HTMLSession()
r = sessions.get(formattedURL[4])
print(r.status_code) #sanity check

XPATH_NAME = '//*[@class="jobViewJobTitleWrap"]//text()'
XPATH_COMPANY = '//*[@class="strong ib"]//text()'
XPATH_LOC = '//*[@class="subtle ib"]//text()'
XPATH_SALARY = ".//*[@class='salEst']//text()"
XPATH_EVERYTHING = '//*'
XPATH_RATING = '//*[@class="ratingNum"]//text()'


for this_url in formattedURL:	
	response = sessions.get(this_url)
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
	