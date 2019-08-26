# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import logging as log

class CrawlerPipeline(object):

    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["scryx"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        dict_item = dict(item)
        self.db.request.update({"_id": dict_item.pop('id')}, {"$push": {"crawler": dict_item }})
        return item
