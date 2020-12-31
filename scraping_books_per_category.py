#! /usr/bin/venv python3
# coding: utf-8

"""
This module is used to scrape all books of a category, including the case that
the category has many pages.
"""

import re
import requests
from bs4 import BeautifulSoup

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


def has_next(soup: BeautifulSoup) -> (bool, str):
    """Check if the current page has a link to go to the next page."""

    res = soup.find('li', class_="next")
    return res is not None, res


def get_next_page(current_url: str, soup: BeautifulSoup) -> str:
    """Retrieve the link of the next page if this exists."""

    res, class_next = has_next(soup)
    next_url = None
    if res:
        href = class_next.a['href']
        current_suffix = current_url.rsplit('/', 1)[-1]
        next_url = current_url.replace(current_suffix, href)
    return next_url


def get_all_book_links_per_category(url: str) -> list:
    """Find all book links in a given url."""

    all_book_links = []
    res = True
    while res:
        # Get all book links of a category page
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            book_names = soup.find_all('a', href=re.compile('^../../../'),
                                       title=re.compile('.*'))

            prefix = "http://books.toscrape.com/catalogue/"
            for book in book_names:
                book_link_split = book['href'].split("../../../", 1)
                book_link = prefix + book_link_split[-1]
                all_book_links.append(book_link)

            # Check if the current page has the next page
            res = has_next(soup)[0]
            if res:
                url = get_next_page(url, soup)
            return all_book_links
        else:
            raise Exception("Error on getting url")

