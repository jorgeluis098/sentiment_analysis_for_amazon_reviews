from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
from scrapping.tools.data_saver import DataSaver

class ProductPage(object):
    def __init__(self, name, url_base, href):
        self.name = name
        self.url_base = url_base
        self.href = href
        self.data_saver = DataSaver()
        self.save_object()

    def search_by(self):
        return
        
    def save_object(self):
        self.data_saver.product_page_append(self.name,self.get_url())

    def get_url(self):
        return self.url_base + self.href