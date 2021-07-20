# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst

# example for work with selectors
# def apply_selector(text):
#     sel = scrapy.Selector(text=text)
#     sel.xpath()
#     ...


def clean_name(string_array):
    return " ".join(map(lambda x: x.strip(), string_array)).strip()


def clean_string(s):
    return s.strip()


class AvitoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=Compose(clean_name), output_processor=TakeFirst()
    )
    price = scrapy.Field(input_processor=MapCompose(clean_string))
    img_urls = scrapy.Field()
    img_info = scrapy.Field()
    # only first url
    # img_urls = scrapy.Field(input_processor=MapCompose(clean_string),
    # output_processor=TakeFirst())
