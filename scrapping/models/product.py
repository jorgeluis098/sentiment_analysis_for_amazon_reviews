from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
from scrapping.tools.data_saver import DataSaver

class Product(object):
    def __init__(self, name, url_base, href, save_data=True):
        super().__init__()
        self.name = name
        self.url_base = url_base
        self.href = href
        if save_data:
            self.data_saver = DataSaver()
            self.save_object()
            
    def get_url(self):
        return self.url_base + self.href

    def save_object(self):
        self.data_saver.product_append(self.name,self.url_base + self.href)
    