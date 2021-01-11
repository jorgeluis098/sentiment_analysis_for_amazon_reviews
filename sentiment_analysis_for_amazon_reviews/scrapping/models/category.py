from bs4 import BeautifulSoup
from sentiment_analysis_for_amazon_reviews.scrapping.tools.firefox_selenium import FirefoxScrapping
from sentiment_analysis_for_amazon_reviews.scrapping.models.product_category import ProductCategory
from sentiment_analysis_for_amazon_reviews.scrapping.tools.data_saver import DataSaver

class Category(object):
    """
    This class is for better control when searching for products on Amazon.
    Search all categories or (sub departments) on amazon.com.mx and create Product Categories.
    """
    def __init__(self, name, html_code, href, url_base):
        self.name = name
        print("\t"+self.name)
        self.html_code = html_code
        self.href = href
        self.url_base = url_base
        self.data_saver = DataSaver()
        self.save_object()
        self.elements = []
        try:
            self.set_product_category()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(f"Hubo un problema con {self.name}")
        self.data_saver.save_product_category()

    def save_object(self):
        self.data_saver.category_append(self.name,self.get_url())

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
