import time
import requests
from bs4 import BeautifulSoup

ENDPOINT_URL = "https://www.kinopoisk.ru/popular/films/"
PARAMS = {
    "tab": "all",
    "quick_filters": "serials",
}


class KinopoiskScraper:
    def __init__(self, start_url, params):
        self.start_url = start_url
        self.start_params = params
        self.info_about_films = []

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
        self.paginate(self.start_url, self.start_params)
        for page_number in range(2, 7):
            params = self.start_params
            params["page"] = page_number
            self.paginate(self.start_url, params)

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

    def save_info_about_films(self):
        # TODO
        # with open(...) as f:
        pass

    # only to page 2
    def paginate(self, url, params):
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
            self.info_about_films.append(info)


if __name__ == "__main__":
    scraper = KinopoiskScraper(ENDPOINT_URL, PARAMS)
    scraper.run()
    scraper.save_info_about_films()
