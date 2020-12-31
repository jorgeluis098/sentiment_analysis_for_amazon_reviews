from bs4 import BeautifulSoup
import requests
from scrapping.models.department import Department
from scrapping.tools.data_saver import DataSaver
from scrapping.models.product_page import ProductPage
from pandas import read_csv

class AmazonSacrapping(object):
    def __init__(self):
        super().__init__()
        self.url_base="https://www.amazon.com.mx/"

    def get_all_categories(self, not_included=["Amazon Prime Video", "Amazon Music", "Echo y Alexa", "Amazon Fire TV", "E-readers y eBooks Kindle"]):
        url = self.url_base + "gp/site-directory?ref_=nav_em__allcategories_0_1_1_30"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all(id="shopAllLinks")
        categories = table[0].find_all("div", class_="popover-grouping")
        all_categories = []
        for categ in categories:
            topic = categ.find_all("h2")[0]
            if not topic.text in not_included:
                all_categories.append(Department(topic.text, categ, self.url_base))
        self.amazon_tree = all_categories
        data_saver = DataSaver()
        data_saver.save_department()
        return all_categories

    def set_url(self,url):
        self.current_url = url

    def get_page(self):
        response = requests.get(self.current_url)
        return BeautifulSoup(response.content, 'html.parser')

    def load_product_page(self, path, id_partition=-1 , partition=3):
        df = read_csv(path)
        product_pages = []
        import pdb;pdb.set_trace()
        partition = self.get_partition(list(df.iterrows()),id_partition,partition)
        for row in partition:
            url_base = "https://www.amazon.com.mx/"
            href = "/" + row[1]["link"].replace(url_base,"")
            name = row[1]["Name"]
            try:
                product_pages.append(ProductPage(name, url_base[:-1], href, save_data=False))
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                continue
        return product_pages


    def get_partition(self, data, i, partitions):
        partition = len(data) // partitions
        if i == -1:
            return data
        if i == partitions - 1:
            return data[i * partition : ]
        else:
            return data[i * partition : (i+1) * partition]

    
