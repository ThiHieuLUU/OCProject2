#! /usr/bin/venv python3
# coding: utf-8

"""This module is used to extract some of the following information of a
book from its url:

product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url
"""

import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ("
    "KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
}


def get_book_info(book_url: str) -> dict:
    """Retrieve some information of a book from it's url and save in a
    dictionary (here, book_info).
    """

    response = requests.get(book_url, headers=HEADERS)
    # To deal with Weird characters, using decode("utf-8")
    soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")

    # Get the article url
    book_info = {"product_page_url": book_url}

    # Find the universal product code of article
    upc = book_url.split(sep="/")[4].split(sep="_")[-1]
    book_info["universal_product_code"] = upc

    # Find the title of article
    title = soup.find("li", class_="active").text
    # To deal with some special characters in the title
    bad_chars = [";", ":", "!", "*", "#", "(", ")", "/", ",", "."]
    title = "".join(i for i in title if i not in bad_chars)
    title = title.replace(" ", "_")
    book_info["title"] = title

    # Find some information of article like that: price, number available, etc.
    main_info = soup.find("table", class_=re.compile("table table-striped"))

    # Find the price excluding tax of article
    price_excl_tax = (
        main_info.find("th", string=re.compile(r"Price \(excl\. tax\)"))
        .find_next("td")
        .text
    )
    book_info["price_excluding_tax"] = price_excl_tax

    # Find the price including tax of article
    price_incl_tax = (
        main_info.find("th", string=re.compile(r"Price \(incl\. tax\)"))
        .find_next("td")
        .text
    )
    book_info["price_including_tax"] = price_incl_tax

    # Find the available number of article
    number_available = (
        main_info.find("th", string=re.compile("Availability")).find_next("td").text
    )
    book_info["number_available"] = number_available

    # Find the category of article
    category = soup.find_all("a", href=re.compile("../category/"))[1].text
    book_info["category"] = category

    # Find the star rating
    star_rating = soup.find("p", class_=re.compile("star-rating "))["class"][1]
    book_info["review_rating"] = star_rating

    # Find the product description
    try:
        product_description = soup.find("div", id="product_description").find_next("p").text
        book_info["product_description"] = product_description
    # To deal with AttributeError: 'NoneType'
    except AttributeError:
        book_info["product_description"] = ''

    # Find the image url
    prefix = "http://books.toscrape.com/"
    image_url = soup.find("img")["src"]
    image_url = prefix + image_url.split("/", 2)[-1]
    book_info["image_url"] = image_url
    return book_info
