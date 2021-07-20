# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy

# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline


class AvitoImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["img_urls"]:
            for img_link in item["img_urls"]:
                try:
                    yield scrapy.Request(img_link)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print("item_completed")
        print()
        if results:
            item["img_info"] = [x[1] for x in results if x[0]]
        if item["img_urls"]:
            del item["img_urls"]
        return item


class AvitoscraperPipeline:
    def process_item(self, item, spider):
        print("PIPELINE")
        print()
        return item
