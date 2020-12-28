from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
from scrapping.models.product_page import ProductPage

class ProductCategory(object):
    def __init__(self, name, href, url_base):
        self.name = name
        self.href = href
        self.url_base = url_base
        self.elements = []
        self.set_products()

    def get_url(self):
        return self.url_base + self.href

    def set_product_page(self, all_products):
        browser = self.browser
        new_url = self.url_base + all_products
        browser.open_url(new_url)
        page = BeautifulSoup(browser.get_html_content(), 'html.parser')
        sidebar = page.find_all("div", id="s-refinements")[0]
        department = sidebar.find_all("li", class_="a-spacing-micro s-navigation-indent-1")[0]
        name = page.find_all("span", class_="a-size-base a-color-base a-text-bold")[1].text
        self.elements.append(ProductPage(name, self.url_base, all_products))
        return 

    def set_products(self):
        url = self.get_url()
        browser = FirefoxScrapping()
        self.browser = browser
        browser.open_url(url)
        page = BeautifulSoup(browser.get_html_content(), 'html.parser')
        footer = page.find_all("div", class_="a-box a-text-center apb-browse-searchresults-footer")[0]
        a_all_products = footer.find_all('a', href=True)[0]
        all_products = a_all_products["href"]
        self.set_product_page(all_products) 
    def get_elements(self):
        return self.elements