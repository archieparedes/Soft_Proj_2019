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



#Formatted XPATHS
XPATH_NAME = './/a/text()'
XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
XPATH_LOC = './/span[@class="subtle loc"]/text()'
XPATH_SALARY = './/span[@class="green small"]/text()'

companyNameFormatted = r.html.xpath(XPATH_COMPANY)
locationFormatted = r.html.xpath(XPATH_LOC)

print(''.join(companyNameFormatted).strip('–'))
print('\n\n\n')

print(' '.join(locationFormatted).strip())


















#create a list of job listings
#job_listings = document.xpath('//li[@class="jl"]')
#create a list of company names
#company_names = document.xpath('.//div[@class="flexbox empLoc"]/div/text()')

#print ('Jobs: ', job_listings)
#print('Companies: ', company_names)