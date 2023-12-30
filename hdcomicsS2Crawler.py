import requests
import sys
import re
from bs4 import BeautifulSoup as bs

start = 0
end = 0
if len(sys.argv) == 3:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
else:
    print("인수가 부족하거나 너무 많습니다.")
    sys.exit()

def num(text):
    numbers = re.search(r'(\d+)화', text)

    # 결과 출력
    if numbers:
        result = int(numbers.group(1))
        return result  # 출력: 4848
    else:
        return 0

total_content = 0
title_list = []


for i in range(start, end+1):
    url = f'https://hdhd275.net/wt/%EC%99%84%EA%B2%B0?gbun=&wpage=&page={i}'
    print(url) 

    response = requests.get(url)    

    html_text = response.text


    soup = bs(html_text, 'html.parser')

    div = soup.find_all('div', 'list-row')
    n = 0
    for d in div:
        n += 1
        print(f'{i}페이지 {n}번째')
        try:
            a = d.find('a')
            toon_url = a.get('href')
            print(toon_url)
            toon_response = requests.get(toon_url)
            toon_html = toon_response.text
            toon_soup = bs(toon_html, 'html.parser')
            
            top = toon_soup.find('tr', 'tborder')
            title = top.find('span').text
            total_content += num(title)
            print(total_content)
        except:
            pass