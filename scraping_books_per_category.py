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
# has 1 page
url ='http://books.toscrape.com/catalogue/category/books/classics_6/index.html'

# has many pages
# url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
# url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

def hasNext(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('li', class_="next")
    if result is None:
        return False
    else:
        return True

def getNextPage(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('li', class_="next")
    print(result)
    if result is not None:
        result =result.a['href']
        suffix = url.rsplit('/', 1)[-1]
        next_url = url.replace(suffix, result)
        # print(next_url)
        return next_url


# res =getNextPage(url)
# print(res)
nbr_pages = 0
all_book_links = {}
res = True
i = 1
while res == True :
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.prettify())

    book_names = soup.find_all('a', href=re.compile('^../../../'), title=re.compile('.*'))
    # print(len(book_names))
    # print(book_names)

    print(url)
    # Find the link of each book in a page (a given url)
    prefix = "http://books.toscrape.com/catalogue/"
    links = []
    for book in book_names:
        book_link_split = book['href'].split(sep="/")
        book_link = prefix + book_link_split[-2] + "/" + book_link_split[-1]
        # print(book_link)
        links.append(book_link)

    all_book_links['page ' + str(i)] = links

    res = hasNext(url)
    # print("res =", res)
    if res :
        i += 1
        url = getNextPage(url)

for key in all_book_links:
    print(f'{key}, number of books: {len(all_book_links[key])}.')
    print(all_book_links[key])




