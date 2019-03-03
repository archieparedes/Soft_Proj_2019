# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    
def pages():
    jobList = list()
    job = input("Enter job title:")
    jobSplit = job.split(" ")

    if(len(jobSplit) == 2):
        baseLink = "https://www.indeed.com/jobs?q={}+{}&sort=date&start=".format(jobSplit[0], jobSplit[1])
    elif(len(jobSplit) == 3):
        baseLink = "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=".format(jobSplit[0], jobSplit[1], jobSplit[2])

    for i in range(0, 2):
        jobList.append(baseLink+"{}0".format(i))

    return jobList