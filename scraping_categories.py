#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to retrieve all categories in the website 'Books to Scrape'.
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

URL = 'http://books.toscrape.com/'


def get_first_link_for_categories(url: str) -> dict:
    """Retrieve all first category links from the url of the Home page."""

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the first links for all categories
    categories = {}
    links = []

    category_links = soup.find('div', class_="side_categories") \
        .find('ul') \
        .find('li') \
        .find('ul') \
        .find_all('a', href=re.compile('catalogue'))

    # Built and get all first category links
    for category_link in category_links:
        links.append(url + category_link['href'])

    for link in links:
        category_name = link.rsplit('/', 2)[-2]
        categories[category_name] = link
    return categories


def save_category_csv(categories: dict) -> None:
    """Create a "csv_data" directory.

    In this directory, book's information is saved for each category in a
    csv file (each csv file name is a category name).
    """

    dir_path = make_directory(CURRENT_DIR_PATH, "csv_data")
    os.chdir(dir_path)
    for category_name, category_link in categories.items():
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

        all_book_links = category.get_all_book_links_per_category(
            category_link)
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for link in all_book_links:
                book_info = book.get_book_info(link)
                writer.writerow(book_info)


def save_category_images(categories: dict) -> None:
    """Create a "images" directory.

    In this directory, book's images are saved for each category in a
    sub-directory (each sub-directory name is a category name).
    """

    parent_dir_path = make_directory(CURRENT_DIR_PATH, "images")
    os.chdir(parent_dir_path)

    for category_name, category_link in categories.items():
        sub_dir_path = make_directory(parent_dir_path, category_name)
        os.chdir(sub_dir_path)
        all_book_links = category.get_all_book_links_per_category(
            category_link)

        for link in all_book_links:
            book_info = book.get_book_info(link)
            image_url, title = book_info['image_url'], book_info['title']
            save_image(image_url, title)


def save_image(image_url: str, title: str) -> None:
    """Download an image from its url and save it in current directory."""

    response = requests.get(image_url)
    img_format = image_url.rsplit(".", 1)[-1]  # jpg, png, etc.
    image_file_name = title + "." + img_format
    img_file = open(image_file_name, "wb")
    img_file.write(response.content)
    img_file.close()


def make_directory(dir_path: str, dir_name: str) -> str:
    """Create a sub-directory from a given directory path and return the
    path of this sub-directory.
    """

    new_dir_path = os.path.join(dir_path, dir_name)
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    return new_dir_path


def demo(nbr_categories: int) -> None:
    """For a demo."""

    categories = get_first_link_for_categories(URL)
    keys = list(categories.keys())
    keys_ = keys[0:nbr_categories:1]
    print(keys_)
    categories_ = {key: categories[key] for key in keys_}
    print(categories_)
    # scrape categories and save results to csv_data directory and images directory
    print("Start of saving csv")
    save_category_csv(categories_)
    print("End of saving csv")
    print("=" * 10)
    print("Start of saving images")
    save_category_images(categories_)
    print("End of saving images")


def main() -> None:
    """For running the project."""

    # Scrape categories and save results to csv_data directory and images directory.
    categories = get_first_link_for_categories(URL)
    print("Start of saving csv")
    save_category_csv(categories)
    print("End of saving csv")
    print("=" * 10)
    print("Start of saving images")
    save_category_images(categories)
    print("End of saving images")


if __name__ == "__main__":
    # For demo
    # nbr_categories = 2
    # demo(nbr_categories)

    # For running the project
    main()

