from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup

class ProductPage(object):
    def __init__(self, name, url_base, href):
        self.name = name
        self.url_base = url_base
        self.href = href

    def search_by(self):
        return
