import requests
from bs4 import BeautifulSoup
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
"""
Écrivez un article Python qui visite cette page et en extrait les informations suivantes :

    product_page_url*
    universal_ product_code (upc) ?
    title *
    price_including_tax *
    price_excluding_tax *
    number_available
    product_dearticleion
    category
    review_rating
    image_url
"""

# Some url for test

# url = 'http://books.toscrape.com/catalogue/under-the-tuscan-sun_504/index.html'
# url = 'http://books.toscrape.com/catalogue/vagabonding-an-uncommon-guide-to-the-art-of-long-term-world-travel_552/index.html'
url = 'http://books.toscrape.com/catalogue/the-golden-condom-and-other-essays-on-love-lost-and-found_637/index.html'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
# print(response)
# print(soup.prettify())

# ? product_page_url
print("Product page url: ", url)

# universal_ product_code (upc) ? extract from url or from soup
upc  = url.split(sep="/")[4].split(sep="_")[-1]
print("Universal product code :", upc)

# Find the title of article
title = soup.find('li', class_="active").text
print("Title: ", title)

# Find some information of article like that: type, price
info_book = soup.find('table', class_=re.compile("table table-striped"))

# Find the product type of article
product_type = info_book.find('th', string="Product Type").find_next('td').text
print("Product type: ", product_type)

# Find the price excluding tax of article
price_excl_tax = info_book.find('th', string=re.compile('Price \(excl\. tax\)')).find_next('td').text
print("Price excluding tax: ", price_excl_tax)

# Find the price including tax of article
price_incl_tax = info_book.find('th', string=re.compile('Price \(incl\. tax\)')).find_next('td').text
print("Price including tax: ", price_incl_tax)

# Find the available number of article
number_available = info_book.find('th', string=re.compile('Availability')).find_next('td').text
print("Number of available articles: ", number_available)

# Find the category of article
category_book = soup.find_all('a', href=re.compile('../category/'))[1].text
# index [0] is always assigned to Book (http://books.toscrape.com/catalogue/category/books_1/index.html )
print("Category: ", category_book)

star_rating = soup.find('p',class_ =re.compile("star-rating "))['class'][1]
# ['star-rating', 'Three']
print("Star rating: ", star_rating)