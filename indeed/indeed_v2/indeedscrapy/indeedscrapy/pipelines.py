# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy.exceptions import DropItem


class IndeedscrapyPipeline(object):
    def __init__(self):
        with open('link-loc-title.csv ', 'r') as f:
            self.seen = set([row for row in f])

        self.file = open('link-loc-title.csv ', 'a+')

    def process_item(self, item, spider):
        link = item['link']

        if link in self.seen:
            raise DropItem('Duplicate link found %s' % link)

        self.file.write(link)
        self.seen.add(link)

        
        return set(item)
