from scrapping.request_scrapping import AmazonSacrapping
from os import path
from pandas import read_csv

data = list(range(1516))
data_path = path.join("scrapping_data","product_page","data.csv")

i = 2
scrapper = AmazonSacrapping()
product_pages = scrapper.load_product_page(data_path, id_partition=i, partition = 4)
products = []
for page in product_pages:
    products_page = page.get_products()
    if products_page:
        products += products_page
