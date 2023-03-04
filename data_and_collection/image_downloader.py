# Quick thrown together image downloader for the CSV files from webscraper

import urllib.request as urllib
import csv
import re

data = []
with open('data_pokemon.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.urlretrieve(url, full_path)
    print("downloaded", file_name)


def filter_strings(item):
    if "," not in item and " " not in item and "[" not in item and "]" not in item:
        return item
    else:
        return ""


for row in data:
    if (row[0] != "Index"):
        title = row[1]
        title = re.sub("[/|*]", "", title)
        images = row[2]
        images2 = re.findall('([^\']*)', images)
        images2 = [filter_strings(x) for x in images2]
        count = 0
        for image in images2:
            if image != "" and image != "set()":
                download_image(image, '../images/pokemon_cards/', title + "(" + str(count) + ")")
                count += 1