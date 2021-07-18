from bs4 import BeautifulSoup
from requests import get
import csv

MAX_NUM_PAGES = 10


# add products
def scraper_products():
    url_site = 'https://www.pichshop.ru'
    response = get(url_site + '/catalog/komu/')
    html_soup = BeautifulSoup(response.text, 'html.parser')

    categories = html_soup.find('div', class_='catalog-categories').findAll('a')

    category_links = []
    category_texts = []

    user_id = 0

    for i in range(len(categories)):
        category_links.append(categories[i].get('href'))
        category_texts.append(categories[i].text)

    section = 1

    with open('products.csv', 'w') as csv_file:

        fieldnames = ['id', 'name', 'description', 'section', 'price', 'images', 'link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(categories)):

            for page_num in range(1, MAX_NUM_PAGES):
                response_category = get(url_site + category_links[i] + '?PAGEN_3={page_num}')
                html_code = BeautifulSoup(response_category.text, 'html.parser')

                products = html_code.find('div', class_='catalog-products-list').findAll('div', class_='product-card')

                for j in range(len(products)):
                    images = 'https:' + products[j].get('data-image')
                    name = products[j].get('name')
                    price = products[j].get('price')
                    link = 'https://www.pichshop.ru' + products[j].get('data-href')
                    description = products[j].findAll('meta')[2].get('content')
                    csv_row = {'id': user_id, 'name': name, 'description': description, 'section': section,
                               'price': price, 'images': images, 'link': link}

                    writer.writerow(csv_row)

                    user_id += 1

            section += 1


scraper_products()
