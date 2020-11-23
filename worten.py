from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import re
import webbrowser
import pandas as pd
from selenium import webdriver

from datetime import date

dr = webdriver.Firefox()





url = 'https://www.worten.pt/informatica-e-acessorios/monitores/monitores-pc?dimensao-ecra=24.5%E2%80%99%E2%80%99%20a%2027.5%E2%80%99%E2%80%99&dimensao-ecra=27.5%E2%80%99%E2%80%99%20a%2030%E2%80%99%E2%80%99&dimensao-ecra=30_27__27_%20a%2040_27__27_&page=1&sort_by=price&order_by=asc'

dr.get(url)
soup = BeautifulSoup(dr.page_source,"lxml")

#page = requests.get(url)
#soup = BeautifulSoup(page.content, 'html.parser')


items = soup.find_all('div', class_='w-product__wrapper')
df = pd.DataFrame(columns=['Title', 'Current Price', 'Old Price', 'Diff', 'Date'])

count = 0
for page in range(6):
    current_page = page+1
    url = 'https://www.worten.pt/informatica-e-acessorios/monitores/monitores-pc?dimensao-ecra=24.5%E2%80%99%E2%80%99%20a%2027.5%E2%80%99%E2%80%99&dimensao-ecra=27.5%E2%80%99%E2%80%99%20a%2030%E2%80%99%E2%80%99&dimensao-ecra=30_27__27_%20a%2040_27__27_&page='+str(current_page)+'&sort_by=price&order_by=asc'
    dr.get(url)
    soup = BeautifulSoup(dr.page_source,"lxml")
    for item in list(items):
        title = item.find('h3', class_='w-product__title').text
        print(title)
        #current_price_span = item.find('span', class_='w-currentPrice iss-current-price') w-currentPrice iss-current-price
        
        prices = item.find_all('span', class_='w-product-price__main')
        current_price = 0
        old_price = 0
        diff = 0
        if len(prices) >= 1:
            current_price = int(prices[0].text)
        if len(prices)>= 2:
            old_price = int(prices[1].text)
            diff = old_price - current_price
        print(current_price, old_price, diff)
        new_entry = [[title, current_price, old_price, diff, date.today().strftime("%d/%m/%Y")]]
        df1 = pd.DataFrame(new_entry,  columns=['Title', 'Current Price', 'Old Price', 'Diff', 'Date'])
        df = df.append(df1)

print(count)
dr.close()

df.to_csv('worten.csv', index=False,   mode='a', header=False)