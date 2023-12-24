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

root_url = r"https://wfwf287.com/ing"
site_title = "늑대닷컴"


def main():
    items = []

    driver = driver_util.create_driver()
    try:

        driver.get(root_url)

        time.sleep(1)

        week_a = driver.find_elements(By.CSS_SELECTOR, "#content > div.group > div.tab.tab9.tab-day.active > a")

        for i in range(1, len(week_a)):

            week_a = driver.find_elements(By.CSS_SELECTOR, "#content > div.group > div.tab.tab9.tab-day.active > a")

            a = week_a[i]
            a.click()

            time.sleep(1)

            li_list = driver.find_elements(By.CSS_SELECTOR, "#content > div.group > div.webtoon-list > ul > li")

            for li in li_list:
                url = li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                soup = BeautifulSoup(li.get_attribute('outerHTML'), 'html.parser')

                # <span> 태그 제거
                for span_tag in soup.select("p.subject > span"):
                    span_tag.extract()

                title = soup.select_one("p.subject").text.strip()

                episode_tag = soup.select_one("div.txt > p:nth-child(3)")

                if episode_tag:
                    episode_text = episode_tag.text
                    match = re.search(r'(\d+)', episode_text)
                    if match:
                        count = int(match.group(1))

                        web_toon_item = WebToon(title, count, url)
                        items.append(web_toon_item)
                        print(web_toon_item)

    except:

        pass

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)


    # 완결
    items = []

    try:
        driver.get(r"https://wfwf287.com/end")

        time.sleep(1)

        category_a = driver.find_elements(By.CSS_SELECTOR, "#content > div.group > div.tab.tab8.mg.tab-genre1.active > a")

        for i in range(len(category_a)):

            category_a = driver.find_elements(By.CSS_SELECTOR,
                                              "#content > div.group > div.tab.tab8.mg.tab-genre1.active > a")

            a = category_a[i]
            a.click()

            time.sleep(1)

            li_list = driver.find_elements(By.CSS_SELECTOR, "#content > div.group > div.webtoon-list > ul > li")

            for li in li_list:
                url = li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                soup = BeautifulSoup(li.get_attribute('outerHTML'), 'html.parser')

                # <span> 태그 제거
                for span_tag in soup.select("p.subject > span"):
                    span_tag.extract()

                title = soup.select_one("p.subject").text.strip()

                episode_tag = soup.select_one("div.txt > p:nth-child(3)")

                if episode_tag:
                    episode_text = episode_tag.text
                    match = re.search(r'(\d+)', episode_text)
                    if match:
                        count = int(match.group(1))

                        web_toon_item = WebToon(title, count, url)
                        items.append(web_toon_item)
                        print(web_toon_item)

    except:
        pass

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)




if __name__ == "__main__":
    main()
