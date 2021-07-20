import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from avito.avitoscraper.items import AvitoscraperItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.avito.ru/krasnodar?q={query}"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath('//a[contains(@class, "-item-title")]')
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        # get only the first element with this xpath
        price_xpath = '(//span[contains(@class, "price-value")]//text())[1]'
        name_xpath = "//h1//text()"
        # big_image_xpath = '//div[contains(@class, ' \
        #                   '"js-gallery-img-frame")]//img/@src'
        small_image_xpath = (
            '//div[contains(@class, "gallery-list-item-link")]//img/@src'
        )

        # item = AvitoscraperItem()
        # item['name'] = response.xpath(name_xpath).get()
        # item['price'] = response.xpath(price_xpath).get()
        # item['img_urls'] = response.xpath(small_image_xpath).getall()
        # yield item

        loader = ItemLoader(item=AvitoscraperItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", name_xpath)
        loader.add_xpath("price", price_xpath)
        loader.add_xpath("img_urls", small_image_xpath)
        yield loader.load_item()
