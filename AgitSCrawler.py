import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium.webdriver.common.by import By
import traceback
import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling
from my_module.webtoon_write_csv import write_webtoons_to_csv

from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = R"https://agit579.xyz"
SITE_TITLE = "아지툰 소설"

def main():
    with driver_util.create_driver() as driver:
        items = []

        driver.get(rf"{ROOT_URL}/novel/")
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#id_np_day_8").click()
        time.sleep(1)

        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            novel_div_list = soup.select("#id_list_novel_p > div")
            all_count = len(novel_div_list)
            print(all_count)
            if all_count < 4510:
                print(len(novel_div_list))
                execute_scrolling(driver)
            else:
                break

        for div in novel_div_list:
            title = div.select_one("a > div > div.col-12.col-6-list-title > h3").text
            url = div.select_one("a")["href"]

            match = re.search(r'location.href="(/novel/list/\d+)"', url)
            if match:
                href_value = match.group(1)
                url = ROOT_URL + href_value

                web_toon_item = WebToon(title, 0, url)
                items.append(web_toon_item)
                print(web_toon_item)

            else:
                print("Not found!")

        driver.implicitly_wait(5)

        for i in range(len(items)):
            driver.get(items[i].url)
            try:
                items[i].count = int(driver.find_element(By.CSS_SELECTOR, "#count_list").text)
                if items[i].count == 0:
                    items[i].count = 1
            except:
                continue
            print(items[i])

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)


        # 완결
        items = []

        driver.get(rf"{ROOT_URL}/novel/")
        time.sleep(1)
        next_button = driver.find_element(By.CSS_SELECTOR, "#id_novel_menu_2 > a")
        next_button.click()
        time.sleep(1)

        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            novel_div_list = soup.select("#id_list_novel_p > div")
            all_count = len(novel_div_list)
            print(all_count)

            if all_count < 13330:
                execute_scrolling(driver)
            else:
                break

        for div in novel_div_list:
            title = div.select_one("a > div > div.col-12.col-6-list-title > h3").text
            url = div.select_one("a")["href"]

            match = re.search(r'location.href="(/novel/list/\d+)"', url)
            if match:
                href_value = match.group(1)
                url = ROOT_URL + href_value

                web_toon_item = WebToon(title, 0, url)
                items.append(web_toon_item)
                print(web_toon_item)

            else:
                print("Not found!")

        driver.implicitly_wait(5)

        for i in range(len(items)):
            driver.get(items[i].url)
            try:
                items[i].count = int(driver.find_element(By.CSS_SELECTOR, "#count_list").text)
                if items[i].count == 0:
                    items[i].count = 1
            except:
                continue
            print(items[i])

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)



if __name__ == "__main__":
    main()
