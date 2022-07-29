from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import keyboard

import time
import logging
logger = logging.getLogger('WDM')
logger.propagate = False
logger.disabled = True

driver = None

def main():
    """
    --- Main
    """
    load_webdriver()

def load_webdriver(headless: bool = False):
    global driver
    WINDOW_SIZE = "1080,900"

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scroll_to_bottom():
    """
    --- Scrolling down to bottom of the page
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def click_button(xpath):
    button = driver.find_element(By.XPATH, value = xpath)
    button.click()

def parse_catalogue(button):
    """
    --- Parsing manga catalogue form remanga
    """
    catalogue_xpath = '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div'
    click_button('//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[' + button + ']')
    scroll_to_bottom()

    parsed_catalogue = driver.find_element(By.XPATH, value = catalogue_xpath)
    parsed_catalogue = parsed_catalogue.text.split('\n')
    parsed_catalogue = parsed_catalogue[1:len(parsed_catalogue):2]
    return parsed_catalogue
    
def get_manga():
    """
    --- Parsing manga catalogues form remanga account
    """
    load_webdriver()
    driver.get("https://remanga.org/manga")
    driver.implicitly_wait(8)
    print("Зайдите в свой аккаунт на сайте, после чего нажмите Enter в консоли...")
    keyboard.wait('Enter')

    click_button('//*[@id="app"]/header/div/button[2]/span[1]/span/div/img')
    click_button('//*[@id="menu-list"]/div/ul/li[1]/a')

    parsed_manga = [parse_catalogue(x) for x in range(1,7)]
    driver.close()
    return parsed_manga

if __name__ == '__main__':
    main()