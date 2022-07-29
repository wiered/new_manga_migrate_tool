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
    driver.get("https://remanga.org/manga")
    driver.implicitly_wait(8)

    print("Зайдите в свой аккаунт на сайте, после чего нажмите Enter в консоли...")
    keyboard.wait('Enter')
    user_btn_xpath = '//*[@id="app"]/header/div/button[2]/span[1]/span/div/img'
    user_btn = driver.find_element(By.XPATH, value = user_btn_xpath)
    user_btn.click()
    user_btn_xpath = '//*[@id="menu-list"]/div/ul/li[1]/a'
    user_btn = driver.find_element(By.XPATH, value = user_btn_xpath)
    user_btn.click()

    print('Доскрольте до конца списка "Читаю" после чего нажмите Enter в консоли...')
    keyboard.wait('Enter')
    manga_list_xpath = '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div'
    manga_list = driver.find_element(By.XPATH, value = manga_list_xpath)
    manga_list = manga_list.text.split('\n')
    manga_list = manga_list[1:len(manga_list):2]

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

def parse_catalogue(button):
    """
    --- Parsing manga catalogue form remanga
    """
    catalogue_xpath = '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div'
    button_xpath = '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[' + button + ']'
    button = driver.find_element(By.XPATH, value = button_xpath)
    button.click()
    scroll_to_bottom()
    parsed_catalogue = driver.find_element(By.XPATH, value = catalogue_xpath)
    parsed_catalogue = parsed_catalogue.text.split('\n')
    parsed_catalogue = parsed_catalogue[1:len(parsed_catalogue):2]
    return parsed_catalogue
    
def get_manga():
    """
    --- Parsing manga catalogues form remanga account
    """
    driver.get("https://remanga.org/manga")
    driver.implicitly_wait(8)
    print("Зайдите в свой аккаунт на сайте, после чего нажмите Enter в консоли...")
    keyboard.wait('Enter')

    button_xpath = '//*[@id="app"]/header/div/button[2]/span[1]/span/div/img'
    button = driver.find_element(By.XPATH, value = button_xpath)
    button.click()

    button_xpath = '//*[@id="menu-list"]/div/ul/li[1]/a'
    button = driver.find_element(By.XPATH, value = button_xpath)
    button.click()

    parsed_manga = [parse_catalogue(x) for x in range(1,7)]
    driver.close()
    return parsed_manga

if __name__ == '__main__':
    main()