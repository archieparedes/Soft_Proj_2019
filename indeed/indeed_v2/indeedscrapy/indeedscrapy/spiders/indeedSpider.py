"""
@author Archie_Paredes
@created Mar 1, 2018
@version 2.0
Indeed - Data Puller - spider
"""
import sys
import scrapy
from scrapy.http.request import Request
from indeedscrapy.items import IndeedscrapyItem, pages
#//div/a[@data-tn-element='jobTitle']/@href
#https://www.indeed.com/jobs?q=data+scientist&start=10


class indeedSpider(scrapy.Spider):
    name = "indeedLinks"

    def __init__(self, job, **kwargs):
        print(job)
        jobSplit = job.split("_")
        if(len(jobSplit) == 2):
            word1 = jobSplit[0]
            word2 = jobSplit[1]
            self.start_urls = ["https://www.indeed.com/jobs?q={}+{}l=&sort=date".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=10".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=20".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=30".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=40".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=50".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=60".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=70".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=80".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=90".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=100".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=110".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=120".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=130".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=140".format(word1,word2),"https://www.indeed.com/jobs?q={}+{}&sort=date&start=150".format(word1,word2),
                            "https://www.indeed.com/jobs?q={}+{}&sort=date&start=160".format(word1,word2)]
        elif(len(jobSplit) == 1):
            word1 = jobSplit[0]
            self.start_urls = ["https://www.indeed.com/jobs?q={}&l=&sort=date".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=10".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=20".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=30".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=110".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=120".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=30".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=130".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=40".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=140".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=50".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=150".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=60".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=160".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=70".format(word1),"https://www.indeed.com/jobs?q={}&sort=date&start=170".format(word1),
                            "https://www.indeed.com/jobs?q={}&sort=date&start=80".format(word1)]
            
        elif(len(jobSplit) == 3):
            word1 = jobSplit[0]
            word2 = jobSplit[1]
            word3 = jobSplit[2]
            self.start_urls = ["https://www.indeed.com/jobs?q={}+{}+{}l=&sort=date".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=90".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=10".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=110".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=20".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=120".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=30".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=130".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=40".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=140".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=50".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=150".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=60".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=160".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=70".format(word1,word2,word3),"https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=170".format(word1,word2,word3),
                            "https://www.indeed.com/jobs?q={}+{}+{}&sort=date&start=80".format(word1,word2,word3)]
            
        else:
            raise Exception("Illegal job input")

        super().__init__(**kwargs)

    def parse(self, response):
        self.log(self.domain)
        links = response.xpath("//div/a[@data-tn-element='jobTitle']/@href").extract()
        titles = response.xpath("//div/a[@data-tn-element='jobTitle']/@title").extract()
        locations = response.xpath("//div[@class='recJobLoc']/@data-rc-loc").extract()
        base = "https://www.indeed.com"
       
        items = []
        for title,li,lo in zip(titles,links,locations):
            print(title)
            item = IndeedscrapyItem()
            item["title"] = title
            item["location"] = lo
            item["link"] = base + li
            if(item in items):
                pass
            else:
                items.append(item)
        return items
            
            
                
        


    
    
