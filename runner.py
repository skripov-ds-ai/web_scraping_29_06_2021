import os

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram_scraper import settings
from instagram_scraper.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    load_dotenv(".env_inst")
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    user_to_parse = os.getenv("USER_TO_PARSE")

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    kwargs = {
        "login": login,
        "password": password,
        "user_to_parse": user_to_parse,
    }
    process.crawl(InstagramSpider, **kwargs)

    process.start()
