"""
@author Archie_Paredes
@created JAN 26, 2018
@version 3.0
Indeed - Pulling Link, Location, Title, Company 1
"""

import csv
import requests

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ur
from urllib.parse import urljoin
import time

one = False
two = False
three = False
jobtitle = input("Enter a job: ")
jobSplit = jobtitle.split(" ")
if(len(jobSplit) == 2):
    two = True
    word1 = jobSplit[0]
    word2 = jobSplit[1]     
    url = "https://www.indeed.com/jobs?q={}+{}&sort=date&start=".format(word1,word2)    
elif(len(jobSplit) == 1):
    one = True
    word1 = jobSplit[0]  
    url = "https://www.indeed.com/jobs?q={}&sort=date&start=".format(word1) 
elif(len(jobSplit) == 3):
    three = True
    word1 = jobSplit[0]
    word2 = jobSplit[1]
    word3 = jobSplit[2]
    url = "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=".format(word1,word2,word3)
else:
    raise Exception("Illegal job input")

titles = list()
companies = list()
links = list()
locations = list()
#description = list()
#requirements = list()

start = time.time()
linkCount = 0

for i in range (0,50): 
    url += "{}0".format(i) # reinitialize url with page number
    res = requests.get(url)
    soup = bs(res.content, "lxml")
    t1 = soup.select('[data-tn-element="jobTitle"]')
    t2 = soup.findAll("div", {"class": "location"})
    t3 = soup.findAll("span", {"class": "company"})
    for link, loc, comp in zip(t1,t2,t3):
        absolute_link = urljoin(url,link.get("href"))
        companies.append(comp.text.strip())
        titles.append(link.get("title"))
        locations.append(loc.text)
        links.append(absolute_link)
        #uClient = ur(absolute_link) #opens site, and gets page
        #pageText = uClient.read() # html
        #uClient.close() #closes sites
        linkCount += 1
        #pageSoup = bs(pageText, "html.parser") #html parser
        
        #description.append(pageSoup.findAll("p"))
        #requirements.append(pageSoup.findAll("li"))
            
    if(one == True):
        url = "https://www.indeed.com/jobs?q={}&sort=date&start=".format(word1) 
    elif(two == True):
        url = "https://www.indeed.com/jobs?q={}+{}&sort=date&start=".format(word1,word2) 
    elif(three == True):
        url = "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=".format(word1,word2,word3)


print("Amount of links: ", linkCount)
print("Writing to CSV")

with open('jobSearch.csv', 'w', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    for t,c,lo,li in zip(titles,companies,locations,links):
        writer.writerow([t,c,lo,li])
 
print("Done writing to CSV")
end = time.time()
print("Execution time: ",end - start)


     

