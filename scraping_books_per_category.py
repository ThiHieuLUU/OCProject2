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


def has_next(current_url):
    """Check if the current page has a link to go to the next page"""
    response = requests.get(current_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('li', class_="next")
    return result is not None


def get_next_page(current_url):
    """Retrieve the link of the next page if this exists"""
    response = requests.get(current_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('li', class_="next")
    if result is not None:
        result = result.a['href']
        suffix = current_url.rsplit('/', 1)[-1]
        next_url = current_url.replace(suffix, result)
        return next_url


def get_all_book_links_per_caterogy(url):
    """Find all links of books in a given url"""
    all_book_links = []
    res = True
    i = 1
    while res:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        book_names = soup.find_all('a', href=re.compile('^../../../'),
                                   title=re.compile('.*'))

        prefix = "http://books.toscrape.com/catalogue/"
        for book in book_names:
            book_link_split = book['href'].split(sep="/")
            book_link = prefix + book_link_split[-2] + "/" + book_link_split[
                -1]
            all_book_links.append(book_link)
        res = has_next(url)
        if res:
            i += 1
            url = get_next_page(url)
    return all_book_links
