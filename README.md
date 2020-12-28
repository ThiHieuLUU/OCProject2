# Project 2
## Goal
Scraping books from the [website](http://books.toscrape.com/)
## About scripts
1. scraping_one_book.py:
	this script is used to extract information of a book. 

2. scraping_books_per_category.py: 
	this script is used to extract all books from a given category, including the case of many pages.

3. scraping_categories.py: 
	this script is used to extract all categories from the home page. 

## Code organization
In this project 2, including:

1. README.md
2. requirements.txt
3. .gitignore
4. scraping_one_book.py
5. scraping_books_per_category.py
6. scraping_categories.py

Where `scraping_one_book.py` and `scraping_books_per_category.py` are imported in `scraping_categories.py`:
```python
import scraping_books_per_category as category
import scraping_one_book as book
```

## Process
1. Create a virtual environment python for the project 2
```bash
sudo pip install virtualenv
mkdir project2
cd project2
virtualenv -p python3 venv
source venv/bin/activate
```
2. Install the packages used for the project
```bash
pip install -r requirements.txt
```
3. Launch
```bash
python3 scraping_categories.py
```

## Results
* "csv_data" directory: save all books's information (one csv file per category)
* "images" directory: save all books's image (one sub image directory per category)






