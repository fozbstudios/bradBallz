# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BradballzPipeline(object):
    def process_item(self, item, spider):
        with open(item['fileName'], "a",encoding='iso-8859-1') as out: #append
            for row in item['lineDict']:
                out.write(row)
        return item
