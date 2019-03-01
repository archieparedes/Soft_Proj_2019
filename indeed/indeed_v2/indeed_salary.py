"""
@author Archie_Paredes
@created JAN 26, 2018
@version 1.0
Indeed - Salary puller
"""

import csv
import re
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ur
from urllib.parse import urljoin

jobList = list()
job = input("Enter job title:")
jobSplit = job.split(" ")

if(len(jobSplit) == 2):
    url = "https://www.indeed.com/jobs?q={}+{}&start=".format(jobSplit[0], jobSplit[1])
elif(len(jobSplit) == 3):
    url = "https://www.indeed.com/jobs?q={}+{}+{}&start=".format(jobSplit[0], jobSplit[1], jobSplit[2])
else:
    raise Exception('Invalid job title')
    

uClient = ur(url)
pageText = uClient.read()
uClient.close()
pageSoup = bs(pageText, "html.parser")

avg = pageSoup.find(attrs={"id": "univsrch-salary-currentsalary"})
minimum = pageSoup.find(attrs={"class": "univsrch-sal-min univsrch-sal-caption float-left"})
maximum = pageSoup.find(attrs={"class": "univsrch-sal-max univsrch-sal-caption float-right"})

avgAmount = ""
minAmount = ""
maxAmount = ""

for i in avg.text:
    if(i.isdigit()):
        avgAmount += i
for i in minimum.text:
    if(i.isdigit()):
        minAmount += i
for i in maximum.text:
    if(i.isdigit()):
        maxAmount += i

with open('dataSciSal.csv', 'w', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Minimum", minAmount])
    writer.writerow(["Average", avgAmount])
    writer.writerow(["Maximum", maxAmount])
    


     

