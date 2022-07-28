from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import keyboard

import logging
logger = logging.getLogger('WDM')
logger.propagate = False
logger.disabled = True

import time

CHROME_PATH = './chrome/chrome'
CHROMEDRIVER_PATH = './chromedriver'
WINDOW_SIZE = "1080,900"

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

def get_list(list, btn_xpath, xpath):
    """
    --- Getting manga lists form remanga
    """
    btn = driver.find_element(By.XPATH, value = btn_xpath)
    btn.click()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    manga_list = driver.find_element(By.XPATH, value = xpath)
    manga_list = manga_list.text.split('\n')
    manga_list = manga_list[1:len(manga_list):2]
    return manga_list
    

def get_manga():
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

    reading_now = get_list('Читаю', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[1]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')
    will_read = get_list('Буду читать', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[2]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')
    read = get_list('Прочитано', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[3]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')
    postponed = get_list('Отложил', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[4]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')
    throw = get_list('Бросил', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[5]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')
    not_interedted = get_list('Не интересно', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/button[6]', '//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div[2]/div')

    driver.close()
    return reading_now, will_read, read, postponed, throw, not_interedted

if __name__ == '__main__':
    main()