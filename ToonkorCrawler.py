import time

import requests
from bs4 import BeautifulSoup

import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write

from my_class.WebToon import WebToon, WebToonCounter

base_url = "https://toonkor289.com"
site_title = "툰코"


def main():
    # current_page(r"https://toonkor289.com/%EC%9B%B9%ED%88%B0/%EC%97%B0%EC%9E%AC")

    legacy_page(r"https://toonkor289.com/%EC%9B%B9%ED%88%B0/%EC%99%84%EA%B2%B0")


def current_page(url):
    driver = driver_util.create_driver()

    items = list()

    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    root_div = soup.select_one("#wt_list > div.dynamicContent > div")
    titles = root_div.find_all("a", id="title")

    for a_tag in titles:
        title = a_tag["alt"]
        web_toon_url = base_url + a_tag["href"]
        count = get_web_toon_count(web_toon_url)

        web_toon_item = WebToon(title, count, web_toon_url)
        items.append(web_toon_item)
        print(web_toon_item)

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)


def legacy_page(url):
    driver = driver_util.create_driver()

    items = list()

    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    root_div = soup.select_one("#wt_list > div.dynamicContent > div.list-container.ajax_load_content")
    titles = root_div.find_all("a", id="title")

    for a_tag in titles:
        title = a_tag["alt"]
        web_toon_url = base_url + a_tag["href"]
        count = get_web_toon_count(web_toon_url)

        web_toon_item = WebToon(title, count, web_toon_url)
        items.append(web_toon_item)
        print(web_toon_item)

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)


def get_web_toon_count(url):
    with requests.Session() as session:  # 세션 사용
        session.headers.update(headers)
        response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    detail_title_text = soup.find("span", class_="tcnt").text
    return int(re.search(r'(\d+)', detail_title_text).group(1))


if __name__ == "__main__":
    main()
