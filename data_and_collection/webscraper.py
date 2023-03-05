#Web scraper that goes through all pages of a given ebay search

import requests
from bs4 import BeautifulSoup
import re
import csv

url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=yugioh+single+cards&_sacat=0&_ipg=240"
def parse_page(url, count, row_count):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    # }
    #Todo headers caused porlems, removed them and it got fixed
    r = requests.get(url)
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

    for link in products_site:
        # print(link)
        r = requests.get(link)
        if r.status_code == 200:
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
            with open('data_yugioh.csv', 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([row_count, Title, image_urls])
                row_count += 1
            print(product)
        else:
            print("Can't access server")



    count += 1
    url = url + "&_pgn=" + str(count)
    parse_page(url, count, row_count)

parse_page(url, 1,0)
