import time

import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

import re
import my_module.create_chrome_driver as driver_util
from my_module.header_util import headers
from my_module.count_wirte_csv import execute_write

from my_class.WebToon import WebToon, WebToonCounter

base_url = "https://newtoki.help/"
site_title = "뉴토끼"


def main():
    root_url = r"https://newtoki.help/%EC%9B%B9%ED%88%B0/%EC%99%84%EA%B2%B0/%EC%9E%A5%EB%A5%B4/%EC%84%B1%EC%9D%B8?sst=wr_datetime"

    items = list()

    try:
        driver = driver_util.create_driver()

        driver.get(root_url)
        time.sleep(5)

        genre_li_list = driver.find_elements(By.CSS_SELECTOR, "#tab2 > ul > li")
        genre_url_list = []

        for li in genre_li_list:
            a_tag = li.find_element(By.CSS_SELECTOR, "a")
            url = a_tag.get_attribute("href")
            genre_url_list.append(url)

        for url in genre_url_list:
            driver.get(url)

            web_toon_list = driver.find_elements(By.CSS_SELECTOR, "#fboardlist > ul > li")

            for li in web_toon_list:
                li_item = li.find_element(By.CSS_SELECTOR, "div.box")
                onclick_text = li_item.get_attribute("onclick")
                link = onclick_text.split("'")[1]

                with requests.Session() as session:  # 세션 사용
                    session.headers.update(headers)
                    response = session.get(link)

                soup = BeautifulSoup(response.content, "html.parser")

                h3_tag = soup.select_one("#content_wrap > div.toon_index > h3")

                if not h3_tag:
                    return 0

                for a in h3_tag.find_all('a'):
                    a.extract()

                title = h3_tag.text.split('|')[0].strip()

                match = re.search(r'(\d+)', h3_tag.text)
                count = int(match.group(1)) if match else 0

                web_toon_item = WebToon(title, count, link)
                items.append(web_toon_item)
                print(web_toon_item)

    except:
        pass

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)


def current_page():
    items = list()

    try:
        driver = driver_util.create_driver()

        driver.get(base_url)
        time.sleep(5)

        week_ul = driver.find_elements(By.CSS_SELECTOR, "#tab1 > ul > li")

        for i in range(1, len(week_ul)):  # 0번째는 제외하기 위해 1부터 시작
            week_ul = driver.find_elements(By.CSS_SELECTOR, "#tab1 > ul > li")
            li = week_ul[i]
            li.click()
            time.sleep(1)

            recent_toon_ul = driver.find_elements(By.CSS_SELECTOR, "#fboardlist > ul > li")

            for web_toon_li in recent_toon_ul:
                li_item = web_toon_li.find_element(By.CSS_SELECTOR, "div.box")
                onclick_text = li_item.get_attribute("onclick")

                link = onclick_text.split("'")[1]
                title_text = li_item.find_element(By.CSS_SELECTOR, ".title > strong").text
                item_count = get_web_toon_count(link)

                web_toon_item = WebToon(title_text, item_count, link)
                items.append(web_toon_item)
                print(web_toon_item)

    except:
        pass

    all_count = WebToonCounter.get_all_count(items)
    execute_write(site_title, all_count)
    print(all_count)


def get_web_toon_count(url):
    with requests.Session() as session:  # 세션 사용
        session.headers.update(headers)
        response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    h3_tag = soup.select_one("#content_wrap > div.toon_index > h3")

    if not h3_tag:
        return 0

    for a in h3_tag.find_all('a'):
        a.extract()

    match = re.search(r'(\d+)', h3_tag.text)

    if match:
        return int(match.group(1))
    else:
        return 0


if __name__ == "__main__":
    main()
