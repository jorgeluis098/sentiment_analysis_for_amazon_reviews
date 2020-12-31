from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
from scrapping.tools.data_saver import DataSaver

class Review(object):
    def __init__(self, review, stars, save_data=True):
        super().__init__()
        self.review = review
        self.stars = stars
        if save_data:
            self.data_saver = DataSaver()
            self.save_object()
            
    def save_object(self):
        self.data_saver.review_append(self.review, self.stars)