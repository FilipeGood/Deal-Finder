from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import re
import webbrowser
import pandas as pd
from selenium import webdriver

from datetime import date

dr = webdriver.Firefox()



url = 'https://www.fnac.pt/Monitores/Monitores-mais-de-27/n21659?sl&ssi=5&sso=1'
df = pd.DataFrame(columns=['Title', 'Current Price', 'Old Price', 'Diff', 'Date'])

#page = requests.get(url)
#soup = BeautifulSoup(page.content, 'html.parser')
#dr.get(url)
#soup = BeautifulSoup(dr.page_source,"lxml")

#items = soup.find_all('div', class_='clearfix Article-item js-Search-hashLinkId')

count = 0
for page in range(6):
    current_page = page+1
    url = 'https://www.fnac.pt/Monitores/Monitores-mais-de-27/n21659?PageIndex='+str(current_page)+'&sl&ssi=5&sso=1'
    dr.get(url)
    soup = BeautifulSoup(dr.page_source,"lxml")

    items = soup.find_all('div', class_='clearfix Article-item js-Search-hashLinkId')
    for item in list(items):
        title = item.find('a', class_='Article-title js-minifa-title js-Search-hashLink').text
        current_price_new = ''
        old_price_new = ''
        current_price = item.find('strong', class_='userPrice')

        if current_price is not None:
            current_price_new = current_price.text

        old_price = item.find('span', class_='oldPrice')
        if old_price is None:
            old_price = item.find('del', class_='oldPrice')
        if old_price is not None:
            count+=1
            old_price_new = old_price.text
        
        if old_price_new == '':
            old_price_new = 0
        else:
            old_price_new = float(old_price_new.replace('€', '').replace(',','.'))

        if current_price_new == '':
            current_price_new = 0
        else:
            current_price_new = float(current_price_new.replace('€', '').replace(',','.'))
        print('title: ', title)
        print(current_price_new)
        print('old price: ', old_price_new)
        print('*********************************************')
        if old_price_new !=0:
            diff_new = old_price_new - current_price_new
        else:
            diff_new = '-'
        new_entry = [[title, current_price_new, old_price_new, diff_new, date.today().strftime("%d/%m/%Y")]]
        df1 = pd.DataFrame(new_entry,  columns=['Title', 'Current Price', 'Old Price', 'Diff', 'Date'])
        df = df.append(df1)
        count+=1
dr.close()
df.to_csv('fnac.csv', index=False,  mode='a', header=False)



