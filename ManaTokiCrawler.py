import time
import logging
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
import traceback
import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling
from my_module.webtoon_write_csv import write_webtoons_to_csv

from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = r"https://manatoki307.net/comic"
SITE_TITLE = "마나토끼"
SEARCH_URL = r"https://manatoki307.net/comic?publish=&jaum=&tag=&sst=wr_datetime&sod=desc&stx=&artist="


def main():
    with driver_util.create_driver() as driver:
        items = []

        driver.get(ROOT_URL)
        time.sleep(1)

        artist_span = driver.find_element(By.CSS_SELECTOR,
                                          "#at-main > section > div.list-tsearch > form > table > tbody > tr:nth-child(2) > td > span")
        artist_span.click()
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        artist_list = [li.text for li in soup.select("#select2-artist-results > li")]
        print(artist_list)

        for artist in artist_list:
            print(artist)
            driver.get(SEARCH_URL + artist)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                webtoon_li_list = soup.select("#webtoon-list-all > li")

                if len(webtoon_li_list) == 0:
                    print("no search")
                    continue

            except Exception as e:
                print("no search")
                print(e)
                continue

            for li in webtoon_li_list:
                title = li.select_one("div > div > div > div.img-wrap > div > div > a > span").text
                url = li.select_one("div > div > div > div.img-wrap > div > div > a")["href"]

                web_toon_item = WebToon(title, 0, url)
                items.append(web_toon_item)
                print(web_toon_item)

        for i in range(len(items)):
            driver.get(items[i].url)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                last_item = soup.select_one("#serial-move > div > ul > li > div")
                try:
                    count = int(last_item.text)

                except:
                    if last_item.select_one("a"):
                        count = int(last_item.select_one("a").text)

                print(count)
                count = int(count)
                count = count if count == 0 else 1

            except Exception as e:
                print(e)
                traceback.print_exc()
                continue

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)


if __name__ == '__main__':
    main()
