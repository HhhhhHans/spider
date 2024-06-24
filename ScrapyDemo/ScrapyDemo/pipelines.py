# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter


class ScrapydemoPipeline:
    def process_item(self, item, spider):
        return item


class movie_pipeline:
    def open_spider(self, spider):
        if spider.name == 'douban':
            self.file = open('movie.json', 'w', encoding='utf-8')
            self.file.write('[')
            self.first_item = True

    def process_item(self, item, spider):
        if spider.name == 'douban':
            if not self.first_item:
                self.file.write(',')
            self.first_item = False
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
        return item

    def close_spider(self, spider):
        if spider.name == 'douban':
            self.file.write(']')
            self.file.close()

class user_pipeline:
    def open_spider(self, spider):
        if spider.name == 'user':
            self.file = open('out.json', 'w', encoding='utf-8')
            self.file.write('[')
            self.first_item = True

    def process_item(self, item, spider):
        if spider.name == 'user':
            if not self.first_item:
                self.file.write(',')
            self.first_item = False
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
        return item

    def close_spider(self, spider):
        if spider.name == 'user':
            self.file.write(']')
            self.file.close()

