# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class MaoyanPipeline:
    # 爬虫启动是创建maoyan.json
    def open_spider(self, spider):
        self.file = open('maoyantop100.json', 'w')

    # 爬虫关闭时关闭文件
    def close_spider(self, spider):
        self.file.close()

    # 将抓取的数据写入json
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
