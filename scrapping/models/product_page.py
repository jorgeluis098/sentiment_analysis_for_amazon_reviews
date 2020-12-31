from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
from scrapping.tools.data_saver import DataSaver
from scrapping.models.product import Product

class ProductPage(object):
    def __init__(self, name, url_base, href, save_data=True):
        self.name = name
        self.url_base = url_base
        self.href = href
        if save_data:
            self.data_saver = DataSaver()
            self.save_object()
        self.elements = []

    def search_by(self):
        return
        
    def save_object(self):
        self.data_saver.product_page_append(self.name,self.get_url())

    def get_url(self):
        return self.url_base + self.href

    def get_products(self):
        browser = FirefoxScrapping()
        browser.open_url(self.get_url())
        page = BeautifulSoup(browser.get_html_content(), 'html.parser')
        products = page.find_all("a", class_="a-link-normal a-text-normal", href=True) 
        products_product = []
        for product in products:
            href = product["href"]
            name_span = product.find_all("span")
            name = ""
            if len(name_span) > 0:
                name = name_span[0].text
            products_product.append(Product(name, self.url_base[:-1], href))
        self.elements = products_product
        return products_product