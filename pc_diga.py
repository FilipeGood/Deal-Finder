from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import re
import webbrowser
import pandas as pd

url = "https://www.pcdiga.com/catalogo-pcdiga/imagem/monitores/mon_polegadas-35-34-32-31_5-28-27-25-24_5-24?product_list_order=price"
current_page = 1
# https://www.pcdiga.com/catalogo-pcdiga/imagem/monitores/mon_polegadas-35-34-32-31_5-28-27-25-24_5-24?p=1&product_list_order=price
df = pd.DataFrame(columns=['Title', 'Current Price', 'Old Price', 'Diff', 'url'])

for i in range(6):
    url = 'https://www.pcdiga.com/catalogo-pcdiga/imagem/monitores/mon_polegadas-35-34-32-31_5-28-27-25-24_5-24?p='+str(i+1)+'&product_list_order=price'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    titles = list()
    get_titles = soup.find_all('li', class_='product-card')
    for item in get_titles:
        title = item.select('div div div.product-card--title a span')[0].text
        titles.append(title)


    #print(soup.find('div', class_='product-card--value product-card--value-without-discount'))
    prices = soup.find_all('div', class_='product-card--value product-card--value-without-discount')
    count=0
    for item in prices:
        print('\n\n------------------------------')
        url = item.select('a')[0]['href']
        title = titles[count]
        current_price =  item.select('a div div.value--current-price p span.price ')
        old_price =  item.select('a div div.value--old-price p span.price ')
        diff =  item.select('a div div.value--price--label-discount ')
        
        current_price_new = ''
        old_price_new = ''
        diff_new = ''
        if len(current_price) !=0:
            current_price_new = current_price[0].text.replace('€', '')

        if len(old_price) !=0:
            old_price_new = old_price[0].text.replace('€', '')
        
        if len(diff) !=0:
            diff_new = diff[0].text.replace('€', '')
        
        new_entry = [[title, current_price_new, old_price_new, diff_new, url]]
        df1 = pd.DataFrame(new_entry,  columns=['Title', 'Current Price', 'Old Price', 'Diff', 'url'])
        df = df.append(df1)
        print(title)
        count+=1
        
    df.to_csv('pc_diga.csv', index=False)
    
#t(count)