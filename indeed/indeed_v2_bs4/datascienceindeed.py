"""
@author Archie_Paredes
@created MAR 3, 2019
@version 2.0
Indeed API - URL puller - Data Science
"""

import csv
import re
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ur
from urllib.parse import urljoin
import time, signal
from itertools import tee, islice, chain

class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()

signal.signal (signal.SIGALRM, handler)


def now_next(some_iterable): # helps with getting previous and next
    items, nexts = tee(some_iterable, 2)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(items, nexts)

print("Pulling Data")

start = time.time()
tech = {"python":0, "r":0, "jasper":0, "sql":0, "tableau":0, "spotfire":0, "oracle":0,
        "sas":0, "machine learning":0, "spss":0, "power bi":0, "rdms":0, "javascript":0,
        "java":0, "tensorflow":0, "torch":0, "pytorch":0,"cloud":0, "big data":0, "c":0,
        "matlab":0, "api":0, "azure":0, "jupyter":0, "hadoop":0, "data mining":0,
        "excel":0, "spark":0, "theano":0, "scikit":0, "rest":0, "deep learning":0,
        "aws":0, "amazon web":0, "nosql":0, "hive":0, "ruby":0, "pearl":0,
        "ai":0,"numpy":0, "linux":0, "pig":0, "mongodb":0, "keras":0, "docker":0,
        "d3":0, "caffe":0, "github":0, "ssh":0, "kafka":0, "mllib":0, "pandas":0,
        "scipy":0}

techFound = {"python":False, "r":False, "jasper":False, "sql":False, "tableau":False, "spotfire":False, "oracle":False,
        "sas":False, "machine learning":False, "spss":False, "power bi":False, "rdms":False, "javascript":False,
        "java":False, "tensorflow":False, "torch":False, "pytorch":False,"cloud":False, "big data":False, "c":False,
        "matlab":False, "api":False, "azure":False, "jupyter":False, "hadoop":False, "data mining":False,
        "excel":False, "spark":False, "theano":False, "scikit":False, "rest":False, "deep learning":False,
        "aws":False, "amazon web":False, "nosql":False, "hive":False, "ruby":False, "pearl":False,
        "ai":False, "numpy":False, "linux":False, "pig":False, "mongodb":False, "keras":False, "docker":False,
        "d3":False, "caffe":False, "github":False, "ssh":False, "kafka":False, "mllib":False, "pandas":False, "scipy":False}

linkCount = 0
url = "https://www.indeed.com/jobs?q=data+scientist&start="
techs = ""
title = ""
location = ""
company = ""
link = ""
links = list()
titles = list()
companies = list()
with open('ds.csv', 'w+', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Title", "Company", "Location", "Tech"])
    for i in range (0,100):
        url += "{}0".format(i) # reinitialize url with page number
        print("page: ", url)
        res = requests.get(url)
        soup = bs(res.content, "lxml")
        t1 = soup.select('[data-tn-element="jobTitle"]')
        t2 = soup.findAll("div", {"class": "location"})
        t3 = soup.findAll("span", {"class": "company"})
        #t4 = soup.findAll("h2", {"class": "jobtitle"})
        
        for link, loc, comp in zip(t1,t2,t3):
            absolute_link = urljoin(url, link.get("href"))
            company = comp.text.strip()
            title = link.get("title")
            location = loc.text
            if (company in companies and title in titles):
                print("dupe found")
                continue

            titles.append(title)
            companies.append(company)
            links.append(absolute_link)
            signal.alarm(5)
            try:
                uClient = ur(absolute_link)  # opens site, and gets page
                pageText = uClient.read()  # html
                uClient.close()  # closes sites

                linkCount += 1
                pageSoup = bs(pageText, "html.parser")  # html parser
                print(linkCount)
                intro = pageSoup.findAll("p")  # job description
                middle = pageSoup.findAll("li")  # tech
                cont = True
                for i in middle:
                    if (str(i)[3] == ' '):
                        pass
                    else:
                        line = (str(i)[4:-5]).lower()

                        # deletes any special chars. Helps with data collection
                        for k in line.split("\n"):
                            line = re.sub(r"[^a-zA-Z0-9]+", ' ', k)  # replace special characters with space

                        # adds 1 to tech if found
                        for t1, t2 in now_next(line.split()):
                            if (t1 in tech and techFound[t1] == False):
                                # tech[t1] = tech[t1] + 1 # adds a tally
                                if (t1 == "torch" or t1 == "pytorch"):
                                    techs += "pytorch" + " "
                                    pass
                                techs += t1 + " "
                                techFound[t1] = True  # prevents duplicates
                                cont = False
                                break
                            else:
                                try:
                                    twoString = t1 + " " + t2  # finds two string
                                    if (twoString in tech):
                                        twoString = twoString.replace(" ", "_")
                                        tech += twoString + " "
                                        # tech[twoString] = tech[twoString] + 1
                                        techFound[twoString] = True  # prevents duplicates\
                                        cont = False
                                        break
                                except:
                                    pass
                        if (cont == False):
                            break
            except:
                print("oof")
                continue
                writer = csv.writer(csv_file)
            if (techs == "c "):
                techs = "c/c++"
            writer.writerow([title, company, location, techs])
            techs = ""  # reset
            techFound = {x: False for x in techFound}  # reset
        url = "https://www.indeed.com/jobs?q=data+scientist&start="


print("Amount of links: ", linkCount)
end = time.time()
print("Execution time: ",end - start)
