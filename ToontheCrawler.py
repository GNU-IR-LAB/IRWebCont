import requests
from bs4 import BeautifulSoup
import re

def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError : 
        return False
    
if __name__ == "__main__":
    week = ['일','월','화','수','목','금','토','열흘',]
    for day in week:
        url = f"https://toonthe3.biz/?idx=on&day={day}&sort=%EC%B5%9C%EC%8B%A0"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.select('.ended .list-row .section-item-inner .section-item-photo a#title[href]')
        exception = []
        sums = 0
        
        for row in links:
            link = row['href']
            inner_response = requests.get(link)
            inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
            titles = inner_soup.select('.bt_view1 .bt_label .bt_data')
            try:
                a = re.sub(r'[^0-9]', '', titles[0].text)
                print(a)
                sum += int(a)
            except:
                exception.append(titles)
                print(day, ' : ', exception)
                print(day, ' : ', sums)