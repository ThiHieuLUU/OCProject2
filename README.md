I. About scripts:
1. scraping_one_book.py:
	this script is used to extract information of a book. 

2. scraping_books_per_category.py: 
	this script is used to extract all books from a given category, including the case of many pages.

3. scraping_categories.py: 
	this script is used to extract all categories from the home page. 

II. Code organization
- Project name : Projet2, including:

1. README.md
2. requirements.txt
3. .gitignore
4. scraping_one_book.py
5. scraping_books_per_category.py
6. scraping_categories.py

where: scraping_one_book.py and scraping_books_per_category.py are imported in scraping_categories.py

III. Process
1. Create the virtual environment python for projet2 project
- sudo pip install virtualenv
- mkdir projet2
- cd projet2
- virtualenv -p python3 venv
- source venv/bin/activate

2. Install the packages used for the project
- pip install -r requirements.txt

3. Launch
python3 scraping_categories.py

IV. Results:
- "csv_data" directory: save all books's information (one csv file per caterory)
- "images" directory: save all books's image (one sub image directory per caterory)






