import time

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write
from my_module.execute_infinite_scrolling import execute_scrolling

from my_class.WebToon import WebToon, WebToonCounter

ROOT_URL = r"https://www.hodu329.net/"
SITE_TITLE = "호두코믹스"


def main():
    with driver_util.create_driver() as driver:
        try:
            items = []
            driver.get(ROOT_URL)
            time.sleep(30)

            for i in range(9):
                week_li_list = driver.find_elements(By.CSS_SELECTOR, "#nav > li")

                week_li_list[i].click()

                try:
                    alert = Alert(driver)
                    alert.accept()
                except:
                    pass

                web_toon_li_list = driver.find_elements(By.CSS_SELECTOR,
                                                        "#list > div.swiper-slide.swiper-slide-active > ul.webtoon-list > li")

                for li in web_toon_li_list:
                    url = li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    match = re.search(r"'(.*?),", url)
                    if match:
                        url = ROOT_URL + match.group(1)
                        if url.endswith('%27'):
                            url = url[:-3]

                    title = li.find_element(By.CSS_SELECTOR, "a > div > div.item-info > p").text

                    web_toon_item = WebToon(title, 0, url)
                    items.append(web_toon_item)
                    print(web_toon_item)

            for i in range(len(items)):
                try:
                    driver.get(items[i].url)
                    time.sleep(1)

                    last_li = driver.find_element(By.CSS_SELECTOR,
                                                  "#sub > div > div.episode-page > strong > div > div > ul > li")
                    count_text = last_li.find_element(By.CSS_SELECTOR, "p.title").text

                    match = re.search(r"(\d+)화", count_text)
                    if match:
                        count = int(match.group(1))
                        if count == 0:
                            count = 1
                    else:
                        count = 0

                    items[i].count = count
                    print(items[i])

                except:
                    pass

        except Exception as e:
            print(e)

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)


if __name__ == "__main__":
    main()
