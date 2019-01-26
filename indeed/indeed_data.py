"""
@author Archie_Paredes
@created JAN 26, 2018
@version 1.0
Indeed API - data pull from job description
"""


import csv
import json
import re
from bs4 import BeautifulSoup as bs
from urllib.request  import urlopen as ur

#from indeed_word_cloud import *

api_url = "http://api.indeed.com/ads/apisearch?publisher=###########&v=2&limit=100000&format=json"


tech = {"python":0, "r":0, "scala":0, "sql":0, "tableau":0, "spotfire":0, "oracle":0,
        "sas":0, "machine learning":0, "spss":0, "power bi":0, "rdms":0, "javascript":0,
        "java":0, "tensorflow":0, "torch":0, "cloud":0, "big data":0, "c++":0,
        "matlab":0, "api":0, "azure":0, "jupyter":0, "hadoop":0, "data mining":0,
        "excel":0, "spark":0, "theano":0, "scikit-learn":0, "rest":0, "deep learning":0,
        "aws":0, "amazon web services":0, "nosql":0, "hive":0, "ruby":0, "pearl":0,
        "ai":0, "numpy":0, "linux":0, "pig":0, "mongodb":0, "keras":0, "docker":0,
        "d3":0, "caffe":0, "github":0, "ssh":0, "kafka":0}

techFound = {"python":False, "r":False, "scala":False, "sql":False, "tableau":False, "spotfire":False, "oracle":False,
        "sas":False, "machine learning":False, "spss":False, "power bi":False, "rdms":False, "javascript":False,
        "java":False, "tensorflow":False, "torch":False, "cloud":False, "big data":False, "c++":False,
        "matlab":False, "api":False, "azure":False, "jupyter":False, "hadoop":False, "data mining":False,
        "excel":False, "spark":False, "theano":False, "scikit-learn":False, "rest":False, "deep learning":False,
        "aws":False, "amazon web services":False, "nosql":False, "hive":False, "ruby":False, "pearl":False,
        "ai":False, "numpy":False, "linux":False, "pig":False, "mongodb":False, "keras":False, "docker":False,
        "d3":False, "caffe":False, "github":False, "ssh":False, "kafka":False}

testUrl = "https://www.indeed.com/viewjob?jk=f29ecd1fdcf4f511&q=data+scientist&l=Chicagoland+Area%2C+IL%5C&tk=1d25vgce8ag4v803&from=web&advn=9531380306485416&adid=256523568&sjdu=R-T8B-gdF79KMElpWnDwftsdtvq3JzH7iO-UWEpHkxLe8RRf4UbQUlJAaI4Xc1Rjb3PiNQHCbUM6e1qa0jkhg4M4IgU1HO5cLZbYVn_M6M0&acatk=1d25vgfj5af8j800&pub=4a1b367933fd867b19b072952f68dceb&vjs=3"

uClient = ur(testUrl2) #opens site, and gets page
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
            line = re.sub(r"[^a-zA-Z0-9]+", ' ', k)

        # adds 1 to tech if found
        for i in line.split():
            if(i in tech and techFound[i] == False):
                val = tech[i]
                tech[i] = val + 1 
                techFound[i] = True # prevents duplicates
        # ******* PROBLEMS ********** only goes through 1 word

techFound = {x: False for x in techFound}
      

