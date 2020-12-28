from bs4 import BeautifulSoup
from scrapping.tools.firefox_selenium import FirefoxScrapping
from scrapping.models.product_category import ProductCategory

class Category(object):
    def __init__(self, name, html_code, href, url_base):
        self.name = name
        self.html_code = html_code
        self.href = href
        self.url_base = url_base
        self.elements = []
        self.set_product_category()

    def get_url(self):
        return self.url_base[:-1] + self.href

    def get_product_section(self, sections , section_name="Departamento"):
        for section in sections:
            div_header = section.find_all("div", class_="a-section a-spacing-small")[0]
            header_name = div_header.find_all("span")
            if len(header_name)> 0 and header_name[0].text == section_name:
                return section
        return None

    def set_product_category(self):
        url = self.get_url()
        browser = FirefoxScrapping()
        browser.open_url(url)
        page = BeautifulSoup(browser.get_html_content(), 'html.parser')
        sidebar = page.find_all("div", id="s-refinements")[0]
        sections = sidebar.find_all("div", class_="a-section a-spacing-none")
        categories = self.get_product_section(sections).find_all("span", class_="a-list-item")[1:]
        for product_category in categories:
            a_href = product_category.find_all('a', href=True)
            if len(a_href)>0:
                href = a_href[0]["href"]
                name = product_category.find_all('span')[0].text
                self.elements.append(ProductCategory(name,href,self.url_base))
        
    
    def get_elements(self):
        return self.elements
