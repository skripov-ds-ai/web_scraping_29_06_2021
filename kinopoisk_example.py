import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "films"
MONGO_COLL = "serials"
ENDPOINT_URL = "https://www.kinopoisk.ru/popular/films/"
PARAMS = {
    "tab": "all",
    "quick_filters": "serials",
}


class KinopoiskScraper:
    def __init__(self, start_url, params, host, port, db_name, coll_name):
        self.start_url = start_url
        self.start_params = params
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[coll_name]

    def get_html_string(self, url, params):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    @staticmethod
    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    def run(self):
        self.parse_search_page(self.start_url, self.start_params)
        for page_number in range(2, 7):
            params = self.start_params
            params["page"] = page_number
            self.parse_search_page(self.start_url, params)
        self.client.close()

    def get_info_from_element(self, element):
        info = {}
        info["name"] = element.find(
            attrs={"class": "selection-film-item-meta__name"}
        ).text
        info["original_name"] = element.find(
            attrs={"class": "selection-film-item-meta__original-name"}
        ).text
        try:
            rating_element = element.find(attrs={"class": "rating__value"})
            info["rating"] = rating_element.text
            info["rating"] = float(info["rating"])
        except AttributeError as e:
            print(e)
        except ValueError as e:
            print(e)
        return info

    def parse_search_page(self, url, params):
        html_string = self.get_html_string(url, params)
        if html_string is None:
            print("There was an error")
            return

        soup = KinopoiskScraper.get_dom(html_string)
        film_elements = soup.find_all(
            attrs={"class": "desktop-rating-selection-film-item"}
        )
        for element in film_elements:
            info = self.get_info_from_element(element)
            self.collection.insert_one(info)


if __name__ == "__main__":
    scraper = KinopoiskScraper(
        ENDPOINT_URL, PARAMS, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLL
    )
    scraper.run()
