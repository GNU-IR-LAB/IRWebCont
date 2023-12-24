import time

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling

from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = r"https://agit321.com/"
SITE_TITLE = "아지툰"


def main():
    with driver_util.create_driver() as driver:
        # items = []
        #
        # try:
        #     driver.get(ROOT_URL)
        #     time.sleep(2)
        #
        #     for i in range(1, 9):
        #         week_button_list = driver.find_elements(By.CSS_SELECTOR, "#home > div > button")
        #         week_button_list[i].click()
        #         time.sleep(2)
        #
        #         soup = BeautifulSoup(driver.page_source, "html.parser")
        #
        #         web_toon_div_list = soup.select("#toonbook_list > div")
        #
        #         for div in web_toon_div_list:
        #             title_a_tag = div.find("a", class_="toon-link")
        #             title = title_a_tag["title"]
        #             url = title_a_tag["href"]
        #
        #             count_p_tag_text = div.select_one("div.card.card-fluid > div > a > p:nth-child(3)").text
        #             match = re.search(r'(\d{4})', count_p_tag_text)
        #             if match:
        #                 count = int(match.group(1))
        #
        #                 item = WebToon(title, count, url)
        #                 items.append(item)
        #                 print(item)
        #
        # except Exception as e:
        #     print(e)
        #
        # all_count = WebToonCounter.get_all_count(items)
        # execute_write(SITE_TITLE, all_count)
        # print(all_count)

        try:
            items = []

            driver.get(ROOT_URL)
            time.sleep(1)
            end_web_toon_button = driver.find_element(By.CSS_SELECTOR,
                                                      "body > nav > div > div.col-3.col-sm-3.col-md-3.nav_category.nav_category_end > a")
            end_web_toon_button.click()

            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            web_toon_div_list = soup.select("#toonbook_list > div")

            for div in web_toon_div_list:
                title_a_tag = div.find("a", class_="toon-link")
                title = title_a_tag["title"]
                url = title_a_tag["href"]

                count_p_tag_text = div.select_one("div.card.card-fluid > div > a > p:nth-child(3)").text
                match = re.search(r'(\d{4})', count_p_tag_text)
                if match:
                    count = int(match.group(1))

                    item = WebToon(title, count, url)
                    items.append(item)
                    print(item)

        except Exception as e:
            print(e)

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)


if __name__ == '__main__':
    main()
