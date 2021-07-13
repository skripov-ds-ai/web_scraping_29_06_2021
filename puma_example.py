# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = "./chromedriver"

url = "https://ru.puma.com/sportivnye-tovary-dlja-muzhchin.html"

options = webdriver.ChromeOptions()
# options.add_argument("--window-size=200,200")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(url)

button_class = "js-load-more"
ok = True
# while ok:
#     # the first variant
#     time.sleep(1.5)
#     try:
#         button = driver.find_element_by_class_name(button_class)
#         button.click()
#     except Exception as e:
#         print(e)
#         ok = False

# the second variant
timeout = 10
i = 0
while ok:
    try:
        button = WebDriverWait(driver, timeout).until(
            # EC.presence_of_element_located(
            #     (By.CLASS_NAME, button_class)
            # )
            EC.element_to_be_clickable((By.CLASS_NAME, button_class))
        )
        button.click()
        i += 1
        print(f"{i} clicks")
    except Exception as e:
        print(e)
        ok = False

# 1st variant of getting info about items!
items_xpath = "//div[contains(@class, 'product-item')]"
items = driver.find_elements_by_xpath(items_xpath)
items_info = []
for item in items:
    info = {}
    title_tag = item.find_element_by_class_name("product-item__name")
    info["title"] = title_tag.text
    # example
    # title_tag.get_attribute("attribute-name")
    print()

# 2d variant getting info about items
source = driver.page_source
# process source with lxml/BS4
