import time

import requests
from bs4 import BeautifulSoup

import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from lxml import html
import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling

from my_module.webtoon_write_csv import write_webtoons_to_csv
from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = r"https://manamoa70.com/bbs/board.php?bo_table=cartoon&page="
SITE_TITLE = "마나모아"
MAX_PAGE_SIZE = 381


def main():
    with driver_util.create_driver() as driver:
        items = []

        try:

            for i in range(1, MAX_PAGE_SIZE):
                driver.get(f"{ROOT_URL}{i}")
                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, "html.parser")

                web_toon_div_list = soup.select("#fboardlist > div.list-container > div")

                for div in web_toon_div_list:
                    title = div.select_one("div > div > div.img-wrap > div > div > a > font").text
                    url = div.select_one("div > div > div.img-wrap > div > div > a")["href"]

                    web_toon_item = WebToon(title, 0, url)
                    items.append(web_toon_item)
                    print(web_toon_item)

            # for i in range(len(items)):
            #     driver.get(items[i].url)
            #
            #     result = driver.find_element(By.XPATH,
            #                                  r'//*[@id="thema_wrapper"]/div/div[4]/div/div/div[1]/div/section/article/div[3]/ul/li[1]/div[2]/a/text()')
            #
            #     match = re.search(r"(\d+)화", result.text)
            #     if match:
            #         count = int(match.group(1))
            #     else:
            #         count = 1
            #
            #     items[i].count = count
            #     print(items[i])

        except Exception as e:
            print(e)
            traceback.print_exc()

        write_webtoons_to_csv(items, f"{SITE_TITLE}_webtoons.csv")

        # all_count = WebToonCounter.get_all_count(items)
        # execute_write(SITE_TITLE, all_count)
        # print(all_count)


if __name__ == "__main__":
    main()
