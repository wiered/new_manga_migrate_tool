from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import keyboard

import time
import logging
logger = logging.getLogger('WDM')
logger.propagate = False
logger.disabled = True

driver = None

class ReMangaParser:
    def load_webdriver(self, headless: bool = False):
        global driver
        WINDOW_SIZE = "1080,900"

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=%s" % WINDOW_SIZE)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def scroll_to_bottom(self):
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


    def click_button(self, xpath):
        button = driver.find_element(By.XPATH, value = xpath)
        button.click()


    def parse_catalogue(self):
        """
        --- Parsing manga catalogue form remanga
        """
        catalogue_xpath = '//html/body/div/main/div[2]/div/div[2]'
        self.click_button('//html/body/div/main/div[2]/div/div[1]/div[2]/div/button[2]')
        
        parsed_catalogue = []

        print("Scanning your manga catalogue")
        for i in tqdm(range(1, 7)):
            self.click_button('//html/body/div[1]/main/div[2]/div/button/span')
            self.click_button(f'//html/body/div[2]/div/div/ul/li[{i}]')
            self.scroll_to_bottom()

            parsed = driver.find_element(By.XPATH, value = catalogue_xpath)
            parsed = parsed.text.split('\n')
            parsed_catalogue.append(parsed)
            driver.execute_script("window.scrollTo(0, 0);")
        
        return parsed_catalogue


    def get_manga(self):
        """
        --- Parsing manga catalogues form remanga account
        """
        self.load_webdriver()
        driver.get("https://remanga.org/manga")
        driver.implicitly_wait(8)
        try:
            self.click_button('//html/body/div[2]/div[3]/div/div/div[1]/button/span') # click phone app advertisement close button 
        except:
            print("No phone app ad")
        self.click_button('//*[@id="__next"]/div/div/button') # click ok to cookies
        self.click_button('//html/body/div/header/nav/div[3]/button') # click blue login button
        print("Зайдите в свой аккаунт на сайте.")
        login_button = driver.find_element(By.XPATH, value = '//html/body/div/header/nav/div[3]/button')
        WebDriverWait(driver, 120).until( 
            EC.staleness_of(login_button)
        )
        driver.minimize_window()

        self.click_button('//html/body/div/header/nav/div[3]/div[2]') # click account logo
        self.click_button('//html/body/div[2]/div/div/ul/li[1]/a') # click name

        parsed_manga = self.parse_catalogue()
        driver.close()
        return parsed_manga
    