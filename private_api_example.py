import time
from pprint import pprint

import requests

example_url = (
    "https://www.luisaviaroma.com/ru-ru/shop/"
    "%d0%bc%d1%83%d0%b6%d1%87%d0%b8%d0%bd%d1%8b"
    "/%d0%be%d0%b1%d1%83%d0%b2%d1%8c"
    "?lvrid=_gm_i4&Page=2&ajax=true"
)

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Content-Type": "application/json",
    "Referer": "https://www.luisaviaroma.com/ru-ru/shop/"
    "%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B"
    "/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C?lvrid=_gm_i4",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    # "sec-ch-ua": 'Not A;Brand";v="99",
    # "Chromium";v="90", "Google Chrome";v="90',
}

# bad variant
# response = requests.get(example_url, headers=headers)
# print()

with requests.Session() as session:
    session.headers.update(headers)
    init_response = session.get(headers["Referer"])
    time.sleep(2)
    print("INIT DONE!")
    response = session.get(example_url)
    pprint(response.json())
    print()
