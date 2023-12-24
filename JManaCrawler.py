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

ROOT_URL = r"https://kr38.jmana.one/"
SITE_TITLE = "제이마나"
MAX_PAGE_SIZE = 907


def main():
    with driver_util.create_driver() as driver:

        items = []

        driver.get(ROOT_URL)
        time.sleep(1)

        web_toon_page = driver.find_element(By.CSS_SELECTOR,
                                            "body > div.container > div.wrap.left > div.header > div.menu-wrap > ul > li:nth-child(2) > a")
        web_toon_page.click()
        time.sleep(1)

        try:
            for i in range(28, MAX_PAGE_SIZE):
                page_url = rf"https://kr38.jmana.one/comic_list_search?page={i}&tag=&tag_without=&keyword=&author=&chosung=&gubun=&ordering="
                driver.get(page_url)
                print(driver.current_url)
                time.sleep(1)

                web_toon_li_list = driver.find_elements(By.CSS_SELECTOR,
                                                        "body > div.container > div.wrap.left > div.content > div.search-result-wrap > div.img-lst-wrap.col6.stl1 > ul > li")

                with requests.Session() as session:
                    for li in web_toon_li_list:
                        a_tag = li.find_element(By.CSS_SELECTOR, "div > a.tit")

                        title = a_tag.text
                        url = a_tag.get_attribute("href")

                        session.headers.update(headers)
                        response = session.get(url)

                        soup = BeautifulSoup(response.content, "html.parser")
                        time.sleep(1)

                        top_title_a_tag = soup.select_one(
                            "body > div.container > div.wrap.left > div.content > div > div.lst-wrap.stl5 > ul > li > div.top-layout-m > div > a")

                        try:

                            match = re.search(r'(\d+)화', top_title_a_tag.text)

                            if match:
                                count = int(match.group(1))
                            else:
                                count = 1

                            item = WebToon(title, count, url)
                            items.append(item)
                            print(item)

                        except:
                            continue


        except Exception as e:
            print(e)
            traceback.print_exc()

        all_count = WebToonCounter.get_all_count(items)
        execute_write(SITE_TITLE, all_count)
        print(all_count)

        # write_webtoons_to_csv(items, f"{SITE_TITLE}_webtoons.csv")


if __name__ == '__main__':
    main()
