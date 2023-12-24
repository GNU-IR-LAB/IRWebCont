import time

import requests
from bs4 import BeautifulSoup
import traceback

from selenium.webdriver.common.by import By

import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling

from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = "https://blacktoon257.com/"
site_title = "블랙툰"


def main():
    with driver_util.create_driver() as driver:
        # 연재
        items = []
        driver.get(ROOT_URL)
        time.sleep(1)

        for i in range(1, 9):
            week_button = driver.find_elements(By.CSS_SELECTOR, "#home > div > button")
            week_button[i].click()
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            web_toon_div_list = soup.select("#toonbook_list > div")

            for div in web_toon_div_list:
                title = div.select_one("a")["title"]
                url = ROOT_URL + div.select_one("a")["href"]

                web_toon_item = WebToon(title, 0, url)
                items.append(web_toon_item)
                print(web_toon_item)

        for i in range(len(items)):
            driver.get(items[i].url)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                print(soup.select_one("#count_list"))
                count = int(soup.select_one("#count_list").text)
                if count == 0:
                    count = 1

            except Exception as e:
                print(e)
                traceback.print_exc()
                continue

            items[i].count = count
            print(items[i])

        all_count = WebToonCounter.get_all_count(items)
        execute_write(site_title, all_count)
        print(all_count)

        # 완결
        items = []
        driver.get(ROOT_URL)
        complete_btn = driver.find_element(By.CSS_SELECTOR, "#profile-tab")
        complete_btn.click()
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        web_toon_div_list = soup.select("#toonbook_list > div")

        for div in web_toon_div_list:
            title = div.select_one("a")["title"]
            url = ROOT_URL + div.select_one("a")["href"]

            web_toon_item = WebToon(title, 0, url)
            items.append(web_toon_item)
            print(web_toon_item)

        for i in range(len(items)):
            driver.get(items[i].url)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                print(soup.select_one("#count_list"))
                count = int(soup.select_one("#count_list").text)
                if count == 0:
                    count = 1

            except Exception as e:
                print(e)
                traceback.print_exc()
                continue

            items[i].count = count
            print(items[i])

        all_count = WebToonCounter.get_all_count(items)
        execute_write(site_title, all_count)
        print(all_count)


if __name__ == "__main__":
    main()
