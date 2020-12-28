from bs4 import BeautifulSoup
import requests
from scrapping.models.department import Department

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
        return all_categories

    def set_url(self,url):
        self.current_url = url

    def get_page(self):
        response = requests.get(self.current_url)
        return BeautifulSoup(response.content, 'html.parser')
