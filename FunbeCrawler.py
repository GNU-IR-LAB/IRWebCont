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

root_url = r"https://funbe282.com/%EC%9B%B9%ED%88%B0/%EC%97%B0%EC%9E%AC"
site_title = "펀비"

def main():
    items = []
    driver = driver_util.create_driver()
    #
    # try:
    #     driver.get(root_url)
    #
    #     for i in range(8):
    #         week_ul = driver.find_elements(By.CSS_SELECTOR, "#wt_list > div.dynamicContent > div.section-weekday > ul")
    #
    #         ul = week_ul[i]
    #         ul.click()
    #
    #         time.sleep(1)
    #
    #         web_toon_list = driver.find_element(By.CSS_SELECTOR, "#wt_list > div.dynamicContent > div.list-container.ajax_load_content")
    #
    #         soup = BeautifulSoup(web_toon_list.get_attribute('outerHTML'), "html.parser")
    #
    #         web_toon_list = soup.select("div.section-item-wrap")
    #
    #         for div in web_toon_list:
    #             title_link = div.select_one("a#title")
    #             if title_link:
    #                 title = title_link.get('alt')
    #                 href = r"https://funbe282.com/" + title_link.get('href')
    #
    #                 with requests.Session() as session:
    #                     session.headers.update(headers)
    #                     response = session.get(href)
    #
    #                 sp = BeautifulSoup(response.content, "html.parser")
    #                 count_content = sp.select_one("#bo_list_total > span")
    #
    #                 match = re.search(r'총\s+(\d+)\s+화', count_content.text)
    #
    #                 if match:
    #                     total_episodes = int(match.group(1))
    #                     web_toon_item = WebToon(title, total_episodes, href)
    #                     items.append(web_toon_item)
    #                     print(web_toon_item)
    #
    #                 else:
    #                     print("No match found!")
    #
    # except Exception as e:
    #     print(e)
    #
    # all_count = WebToonCounter.get_all_count(items)
    # execute_write(site_title, all_count)
    # print(all_count)


    # 완결

    try:
        driver.get(r"https://funbe282.com/%EC%9B%B9%ED%88%B0/%EC%99%84%EA%B2%B0")
        time.sleep(5)

        web_toon_list = driver.find_element(By.CSS_SELECTOR,
                                            "#wt_list > div.dynamicContent > div.list-container.ajax_load_content")


        soup = BeautifulSoup(web_toon_list.get_attribute('outerHTML'), "html.parser")


        web_toon_list = soup.select("div.list-row")

        for div in web_toon_list:
            title_link = div.select_one("a#title")
            if title_link:
                title = title_link.get('alt')
                href = r"https://funbe282.com" + title_link.get('href')

                with requests.Session() as session:
                    session.headers.update(headers)
                    response = session.get(href)

                sp = BeautifulSoup(response.content, "html.parser")
                count_content = sp.select_one("#bo_list_total > span")

                match = re.search(r'총\s+(\d+)\s+화', count_content.text)

                if match:
                    total_episodes = int(match.group(1))
                    web_toon_item = WebToon(title, total_episodes, href)
                    items.append(web_toon_item)
                    print(web_toon_item)

                else:
                    print("No match found!")

    except Exception as e:
        print(e)

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)








if __name__ == "__main__":
    main()