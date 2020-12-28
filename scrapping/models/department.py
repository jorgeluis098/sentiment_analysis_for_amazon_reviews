from scrapping.models.category import Category
from scrapping.tools.firefox_selenium import FirefoxScrapping

class Department(object):
    
    def __init__(self, name, html_code, url_base):
        self.name = name
        self.html_code = html_code
        self.url_base = url_base
        self.elements = []
        self.set_elements()

    def set_elements(self):
        html = self.html_code
        for element in html.find_all("li"):
            href = element.find_all('a', href=True)[0]["href"] 
            self.elements.append(Category(element.text, element, href, self.url_base))

    def get_elements(self):
        return self.elements
    
    def append_element(self,element):
        self.elements.append(element)
        
    def __str__(self):
        return self.name


