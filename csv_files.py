import pandas as pd


# add products
def make_csv1():
    arr = [[101, 'First product', 'Beautiful', 1, 900, 'https://masyamba.ru/%D0%B2%D0%B5%D1%82%D1%80%D1%8F%D0%BD%D0'
                                                       '%B0%D1%8F-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8/2-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8.jpg']
        , [102, 'Second product', 'Pretty', 2, 1200,
           'https://masyamba.ru/%D0%B2%D0%B5%D1%82%D1%80%D1%8F%D0%BD%D0%B0%D1%8F-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8/48-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8.jpg']
        , [103, 'Third product', 'Good', 2, 10000,
           'https://masyamba.ru/%D0%B2%D0%B5%D1%82%D1%80%D1%8F%D0%BD%D0%B0%D1%8F-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8/16-%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8.jpg']
           ]
    products = pd.DataFrame(arr, columns=['id', 'name', 'description', 'section', 'price', 'images', 'link'])
    products.to_csv('products.csv', index=False, na_rep='Unknown')


data = pd.DataFrame(pd.read_csv('products.csv'),
                    columns=['id', 'name', 'description', 'section', 'price', 'images', 'link'])
data2 = pd.DataFrame()


def open_csv_for_basket():
    global data2
    data2 = pd.read_csv('result.csv', names=['user_id', 'product_id'])
    data2.reset_index(drop=True, inplace=True)