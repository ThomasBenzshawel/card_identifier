#Web scraper that goes through all pages of a given ebay search

import requests
from bs4 import BeautifulSoup
import re
import csv

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=pokemon+single+cards&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=magic+the+gathering+single+cards&_osacat=0&_ipg=240"
def parse_page(url, count, row_count):
    main_url = 'https://www.ebay.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')

    product_list = soup.find_all('div', class_='s-item__image')

    products_site = []

    for item in product_list:
        for link in item.find_all('a', href=True):
            products_site.append(link['href'])
    products_site = list(dict.fromkeys(products_site))
    products_site = list(filter(None, products_site))
    products_site = [x for x in products_site if x.startswith('https://www.ebay.com/itm/')]
    print("Found this many products: ", len(products_site))

    item_list = []
    rows = []
    for link in products_site:
        # print(link)
        r = requests.get(link, headers=headers)
        # print(r)
        soup = BeautifulSoup(r.content, 'html.parser')
        Title = soup.select_one('h1', class_='x-item-title__mainTitle').get_text(strip=True)

        image_urls = [re.sub(r"s-l(\d+)", "s-l2000", i.get('src')) for i in soup.find_all(class_="merch-item-image")]
        if len(image_urls) == 0:

            image_urls = set([x['src'] for x in soup.findAll('img', {'id': 'icImg'})])  # remove duplicate images
        product = {
            "Title": Title,
            "Image_URLS": image_urls
        }
        with open('data_pokemon.csv', 'a', encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([row_count, Title, image_urls])
            row_count += 1
        print(product)



    count += 1
    url = url + "&_pgn=" + str(count)
    parse_page(url, count, row_count)

parse_page(url, 1,0)
