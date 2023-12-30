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

SITE_TITLE = "툰코시즌2"
ROOT_URL = r"https://tkr256.com/wt"


def main():
    with driver_util.create_driver() as driver:
        # driver.get(ROOT_URL)
        # items = []
        #
        # for i in range(1, 9):
        #     week_li_list = driver.find_elements(By.CSS_SELECTOR,
        #                                         "#thema_wrapper > div.at-body > div > div > div.dynamicContent > div.btn-yoil > li")
        #     week_li_list[i - 1].click()
        #     time.sleep(1)
        #
        #     last_page_number = driver.find_elements(By.CLASS_NAME, "pg_page")
        #     try:
        #         last_page_number = last_page_number[-2]
        #
        #     except:
        #         driver.get(r"https://tkr256.com/wt/%EC%97%B0%EC%9E%AC%EC%A4%91/8/all/%EC%B5%9C%EC%8B%A0/%EC%A0%84%EC%B2%B4")
        #         time.sleep(1)
        #
        #         soup = BeautifulSoup(driver.page_source, "html.parser")
        #
        #         webtoon_div_list = soup.select(
        #             "#thema_wrapper > div.at-body > div > div > div.list-container.ajax_load_content > div")
        #
        #         for div in webtoon_div_list:
        #             a_tag = div.select_one("div > div > div.section-item-title > a")
        #             title = a_tag["alt"]
        #             url = a_tag["href"]
        #
        #             web_toon_item = WebToon(title, 0, url)
        #             items.append(web_toon_item)
        #             print(web_toon_item)
        #
        #         break
        #
        #     last_page_number = int(last_page_number.text) + 1
        #
        #     for j in range(1, last_page_number):
        #         search_url = rf"https://tkr256.com/wt/%EC%97%B0%EC%9E%AC%EC%A4%91/{i}/all/%EC%B5%9C%EC%8B%A0/%EC%A0%84%EC%B2%B4?gbun=&wpage=&page={j}"
        #         driver.get(search_url)
        #         time.sleep(1)
        #
        #         soup = BeautifulSoup(driver.page_source, "html.parser")
        #
        #         webtoon_div_list = soup.select(
        #             "#thema_wrapper > div.at-body > div > div > div.list-container.ajax_load_content > div")
        #
        #         for div in webtoon_div_list:
        #             a_tag = div.select_one("div > div > div.section-item-title > a")
        #             title = a_tag["alt"]
        #             url = a_tag["href"]
        #
        #             web_toon_item = WebToon(title, 0, url)
        #             items.append(web_toon_item)
        #             print(web_toon_item)
        #
        # for i in range(len(items)):
        #     driver.get(items[i].url)
        #     time.sleep(1)
        #
        #     inner_soup = BeautifulSoup(driver.page_source, "html.parser")
        #
        #     try:
        #         last_tr = inner_soup.select_one(
        #             "#thema_wrapper > div.at-body > div > div.at-content > div.col-md-9.bt > table.web_list > tbody > tr")
        #
        #         count_text = last_tr.select_one("span").text
        #         print(count_text)
        #         match = re.search(r'^(\d{4})', count_text)
        #
        #         if match:
        #             count = int(match.group(1))
        #             if count == 0:
        #                 count = 1
        #
        #             items[i].count = count
        #             print(items[i])
        #
        #     except:
        #         traceback.print_exc()
        #         continue
        #
        # all_count = WebToonCounter.get_all_count(items)
        # execute_write(SITE_TITLE, all_count)
        # print(all_count)

        # 완결
        items = []
        driver.get(r"https://tkr256.com/wt/%EC%99%84%EA%B2%B0")
        search_url = r"https://tkr256.com/wt/%EC%99%84%EA%B2%B0?gbun=&wpage=&page="

        for i in range(1, 14):
            driver.get(rf"{search_url}{i}")
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            webtoon_div_list = soup.select(
                "#thema_wrapper > div.at-body > div > div > div.list-container.ajax_load_content > div")

            for div in webtoon_div_list:
                a_tag = div.select_one("div > div > div.section-item-title > a")
                title = a_tag["alt"]
                url = a_tag["href"]

                web_toon_item = WebToon(title, 0, url)
                items.append(web_toon_item)
                print(web_toon_item)

        for i in range(len(items)):
            driver.get(items[i].url)
            time.sleep(1)

            inner_soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                tr_list = inner_soup.select("#thema_wrapper > div.at-body > div > div.at-content > div.col-md-9.bt > table.web_list > tbody > tr.tborder")
                items[i].count = len(tr_list)
                print(items[i])

            except:
                traceback.print_exc()
                continue

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)


if __name__ == '__main__':
    main()