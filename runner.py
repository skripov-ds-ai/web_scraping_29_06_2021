from urllib.parse import quote_plus

# from avito.avitoscraper import settings
# from avito.avitoscraper.spiders.avito import AvitoSpider
from otscraper import settings
from otscraper.spiders.otspider import OtSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == "__main__":
    custom_settings = Settings()
    custom_settings.setmodule(settings)

    query = quote_plus("видеокарта NVIDIA".encode(encoding="cp1251"))

    process = CrawlerProcess(settings=custom_settings)
    process.crawl(OtSpider, query=query)
    # process.crawl(AvitoSpider)

    process.start()
