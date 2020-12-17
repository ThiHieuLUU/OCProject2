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

url = 'http://books.toscrape.com/'
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())

# Find the links of all catalogues
links = []
catalogue_links = soup.find('div', class_="side_categories").find_all('a',href=re.compile('catalogue'))


[links.append(url + catalogue_links[i]['href']) for i in range(len(catalogue_links)) ]
[print(links[i] + '\n') for i in range(len(catalogue_links)) ]
