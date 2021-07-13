import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = "./chromedriver"


options = webdriver.ChromeOptions()
# options.add_argument("--window-size=200,200")
options.add_argument("--start-maximized")

url = "https://pikabu.ru/"

driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(url)


for i in range(5):
    time.sleep(2)
    articles = driver.find_elements_by_tag_name("article")
    article = articles[-1]
    actions = ActionChains(driver)
    actions.move_to_element(article)
    # actions.send_keys(Keys.END)
    # example of multiple keyboard buttons
    # Ctrl+C
    # actions.key_down(Keys.CONTROL).key_down("C")\
    #     .key_up(Keys.CONTROL).key_up("C")
    actions.perform()

# driver.execute_script("some js code")
