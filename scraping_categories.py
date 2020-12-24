#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to retrieve all categories
in the website 'Books to Scrape'
"""

import re
import os
import csv

import requests
from bs4 import BeautifulSoup

import scraping_books_per_category as category
import scraping_one_book as book

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36',
           "Upgrade-Insecure-Requests": "1", "DNT": "1", "Accept": "text/html,"
                                                                   "application"
                                                                   "/xhtml+xml,"
                                                                   "application"
                                                                   "/xml;q=0.9,"
                                                                   "*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, "
                                                                   "deflate"}
CURRENT_DIR_PATH = os.getcwd()

url = 'http://books.toscrape.com/'


def get_first_link_for_categories(url):
    """Retrieve all first category links from the url of the Home page"""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    # Find the links of all catalogues
    categories = {}
    links = []
    category_links = soup.find('div', class_="side_categories") \
        .find_all('a', href=re.compile('catalogue'))

    # Built and get all links except the first (book_1: link of the home page)
    [links.append(url + category_links[i]['href']) for i in
     range(1, len(category_links), 1)]

    for link in links:
        category_name = link.rsplit('/', 2)[-2]
        categories[category_name] = link

    # [print(key + ': ' + categories[key] + '\n') for key in categories]
    return categories


def save_category_csv(categories):
    dir_path = make_directory(CURRENT_DIR_PATH, "csv_data")
    os.chdir(dir_path)
    for category_name in categories:
        category_link = categories[category_name]

        file_name = category_name + '.csv'
        fieldnames = ['product_page_url',
                      'universal_product_code',
                      'title',
                      'price_including_tax',
                      'price_excluding_tax',
                      'number_available',
                      'product_description',
                      'category',
                      'review_rating',
                      'image_url']

        all_book_links = category.get_all_book_links_per_caterogy(
            category_link)
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for link in all_book_links:
                book_info = book.get_book_info(link)
                writer.writerow(book_info)


def save_category_images(categories):
    parent_dir_path = make_directory(CURRENT_DIR_PATH, "images")
    os.chdir(parent_dir_path)

    for category_name in categories:
        category_link = categories[category_name]
        sub_dir_path = make_directory(parent_dir_path, category_name)
        os.chdir(sub_dir_path)
        all_book_links = category.get_all_book_links_per_caterogy(category_link)

        for link in all_book_links:
            book_info = book.get_book_info(link)
            image_url, title = book_info['image_url'], book_info['title']
            save_image(image_url, title)


def save_image(image_url, title):
    """Download an image from its url and save it in current directory"""
    response = requests.get(image_url)
    img_format = image_url.rsplit(".", 1)[-1]  # jpg, png, etc.
    image_file_name = title + "." + img_format
    img_file = open(image_file_name, "wb")
    img_file.write(response.content)
    img_file.close()


def make_directory(dir_path, dir_name):
    """Create a directory for each category in order to move all book's images
    into theirs corresponding category
    """
    new_dir_path = os.path.join(dir_path, dir_name)
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    return new_dir_path

def demo(nbr_keys):
    # For demo
    categories = get_first_link_for_categories(url)
    keys = list(categories.keys())
    keys_ = keys[0:nbr_keys:1]
    print(keys_)
    categories_ = {key: categories[key] for key in keys_}
    print(categories_)
    # scrape categories and save results to csv_data directory and images directory.
    print("Start of saving csv")
    save_category_csv(categories_)
    print("End of saving csv")
    print("="*10)
    print("Start of saving csv")
    save_category_images(categories_)
    print("End of saving csv")

def main():
    categories = get_first_link_for_categories(url)
    # scrape categories and save results to csv_data directory and images directory.
    print("Start of saving csv")
    save_category_csv(categories)
    print("End of saving csv")
    print("="*10)
    print("Start of saving csv")
    save_category_images(categories)
    print("End of saving csv")

if __name__ == "__main__":
    # For demo
    nbr_categories = 2
    demo(nbr_categories)

    # For running the project
    # main()






