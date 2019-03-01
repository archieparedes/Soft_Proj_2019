"""
@author Archie_Paredes
@created Mar 1, 2018
@version 2.0
Indeed - Data Puller - spider
"""
import scrapy
from indeedscrapy.items import IndeedscrapyItem
#//div/a[@data-tn-element='jobTitle']/@href
#https://www.indeed.com/jobs?q=data+scientist&start=10

jobList = list()
job = input("Enter job title:")
jobSplit = job.split(" ")

if(len(jobSplit) == 2):
    baseLink = "https://www.indeed.com/jobs?q={}+{}&start=".format(jobSplit[0], jobSplit[1])
elif(len(jobSplit) == 3):
    baseLink = "https://www.indeed.com/jobs?q={}+{}+{}&start=".format(jobSplit[0], jobSplit[1], jobSplit[2])

for i in range(0, 15):
    jobList.append(baseLink+"{}0".format(i))

class indeedSpider(scrapy.Spider):
    name = "indeedLinks"
    start_urls = jobList
    def parse(self, response):
        links = response.xpath("//div/a[@data-tn-element='jobTitle']/@href").extract()
        titles = response.xpath("//div/a[@data-tn-element='jobTitle']/@title").extract()
        locations = response.xpath("//div[@class='recJobLoc']/@data-rc-loc").extract()
        base = "https://www.indeed.com"
        k = 1
        items = []
        for title,li,lo in zip(titles,links,locations):
            item = IndeedscrapyItem()
            item["title"] = title
            item["location"] = lo
            item["link"] = base + li
            items.append(item)
        return items
            
            
                
        


    
    