# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

class DoubanspiderPipeline(object):
    def __init__(self):
        self.file = open('doubanTop250book.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if float(item['score']) < 8.5:
            raise DropItem("Missing score in %s" % item)
        else:
            line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file.write(line)
            return item

    def close_spider(self, spider):
        self.file.close()