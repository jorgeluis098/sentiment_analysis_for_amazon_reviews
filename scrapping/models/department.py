from scrapping.models.category import Category
from scrapping.tools.firefox_selenium import FirefoxScrapping
from scrapping.tools.data_saver import DataSaver

class Department(object):
    """
    This class is for better control when searching for products on Amazon.
    Search all departments on amazon.com.mx and create categories o (sub departments)
    """
    def __init__(self, name, html_code, url_base):
        self.name = name
        print(self.name)
        self.html_code = html_code
        self.url_base = url_base
        self.data_saver = DataSaver()
        self.save_object()
        self.elements = []
        try:
            self.set_elements()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(f"Hubo un problema con {self.name}")
        self.data_saver.save_category()
        

    def save_object(self):
        self.data_saver.department_append(self.name,self.url_base)

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


