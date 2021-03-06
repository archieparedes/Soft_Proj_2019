"""
@author Archie_Paredes
@created Mar 1, 2018
@version 2.0
Indeed - Data Puller - Text examine
"""
import csv
import re
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ur
from urllib.parse import urljoin
import time
from itertools import tee, islice, chain

def now_next(some_iterable): # helps with getting previous and next
    items, nexts = tee(some_iterable, 2)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(items, nexts)

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

with open('link-loc-title.csv') as csvfile:
    reader = csv.reader(csvfile)
    for x in reader:
        try:
            if(x[0] == 'link'):
                pass
            absolute_link = x[0]
            uClient = ur(absolute_link) #opens site, and gets page
            pageText = uClient.read() # html
            uClient.close() #closes sites
            pageSoup = bs(pageText, "html.parser") #html parser

            intro = pageSoup.findAll("p") # job description
            middle = pageSoup.findAll("li") # tech
            for i in middle:
                if(str(i)[3] == ' '):
                    pass
                else:
                    line = (str(i)[4:-5]).lower()

                    # deletes any special chars. Helps with data collection
                    for k in line.split("\n"):
                        line = re.sub(r"[^a-zA-Z0-9]+", ' ', k) # replace special characters with space

                    # adds 1 to tech if found
                    for t1,t2 in now_next(line.split()):
                        if(t1 in tech and techFound[t1] == False): 
                            tech[t1] = tech[t1] + 1 # adds a tally
                            techFound[t1] = True # prevents duplicates
                        else:
                            try:
                                twoString = t1+" "+t2 # finds two string
                                if(twoString in tech):
                                    tech[twoString] = tech[twoString] + 1 
                                    techFound[twoString] = True # prevents duplicates
                            except:
                                pass
                            
            techFound = {x: False for x in techFound}
        except:
            pass
    
torch = 0
aws = 0

with open('techData.csv', 'w', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in tech.items():
        if(key == "aws" or key == "amazon web"):
            aws+=1
        elif(key == "torch" or key == "pytorch"):
            torch+=1
        else:
            writer.writerow([key, value])
    writer.writerow(["amazon web service", aws])
    writer.writerow(["pyTorch", torch])
    

