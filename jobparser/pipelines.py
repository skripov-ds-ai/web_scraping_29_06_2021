# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

from jobparser.settings import MONGO_HOST, MONGO_PORT

# from itemadapter import ItemAdapter


class JobparserPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.vacancies

    # TODO: implement this
    def process_salary(self, salary):
        # None if it is not a number
        return salary[0], salary[0]

    def process_item(self, item, spider):
        # print("Inside pipeline")
        # print()
        s_min, s_max = self.process_salary(item["salary"])
        item["salary_min"], item["salary_max"] = s_min, s_max

        del item["salary"]
        # item.pop("salary")
        # bad example
        # item['source'] = 'hhru'
        # example
        # if spider.name == 'hhru':
        #     pass
        # else:
        #     pass
        item["source"] = spider.name

        # collection = self.db['some_vacancies']
        # TODO: implement without duplicates
        self.db[spider.name].insert_one(item)

        return item

    # closing database conection on closing spider
    def close_spider(self):
        self.client.close()
