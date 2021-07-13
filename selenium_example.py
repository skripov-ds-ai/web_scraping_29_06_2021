import os
import time

# pip install python-dotenv
from dotenv import load_dotenv

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


load_dotenv()


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DRIVER_PATH = "./chromedriver"

url = "https://gb.ru/login"

options = webdriver.ChromeOptions()
# options.add_argument("--window-size=200,200")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(url)

user_mail = driver.find_element_by_id("user_email")
user_mail.send_keys(EMAIL)

user_password = driver.find_element_by_id("user_password")
user_password.send_keys(PASSWORD)
# user_password.send_keys(PASSWORD + "\n")
# user_password.send_keys("\n")
user_password.send_keys(Keys.ENTER)
# time.sleep(10)

url = "https://gb.ru/profile"
driver.get(url)
# time.sleep(5)
city = driver.find_element_by_name("user[city]")
# TODO: fix clearing
city.send_keys("")
city.clear()
# time.sleep(2)
city.send_keys("Рим")

gender = driver.find_element_by_name("user[gender]")
select = Select(gender)
# unknown
# select.select_by_index(0)
# time.sleep(2)
select.select_by_value("female")
# time.sleep(7)
select.select_by_visible_text("Не выбран")
gender.submit()


time.sleep(9)
url = "https://gb.ru/logout"
driver.get(url)

# time.sleep(20)
# close browser?
# driver.close()
driver.quit()
