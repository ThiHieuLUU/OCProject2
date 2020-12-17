import requests
from bs4 import BeautifulSoup
import time
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
"""
Écrivez un article Python qui visite cette page et en extrait les informations suivantes :

    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_dearticleion
    category
    review_rating
    image_url
"""

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())

book_names = soup.find_all('a', href=re.compile('^../../../'), title=re.compile('.*'))
# print(len(book_names))
# print(book_names)

# Find the link of each book in a page
prefix = " http://books.toscrape.com/catalogue/"
for book in book_names:
    book_link_split = book['href'].split(sep="/")
    book_link = prefix + book_link_split[-2] + "/" + book_link_split[-1]
    print(book_link)

