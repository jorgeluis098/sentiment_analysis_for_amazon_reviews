import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from os import path
import platform
from time import sleep

from sentiment_analysis_for_amazon_reviews.scrapping.common.singleton import singleton

@singleton
class FirefoxScrapping(object):
    """
    Wrap of selenium.
    The use of this class is to use the webdriver in whatever class is required.
    It's singleton so as not to instantiate a lo pendejo.
    Args:
        object ([type]): [description]
    """    
    def __init__(self):
        self.set_driver()

    def set_driver(self):
        """
        Set the Linux/Windows Firefox driver.
        Testet: Windows.
        """        
        os_info = platform.system()
        firefox_webdriver_filename=""
        if platform.system() == "Windows":
            firefox_webdriver_filename="geckodriver.exe"
        elif platform.system() == "Linux":
            firefox_webdriver_filename="geckodriver"
        firefox_webdriver_path=path.join("scrapping","tools","webdriver",firefox_webdriver_filename)
        self.driver = webdriver.Firefox(executable_path=firefox_webdriver_path)
    
    def open_url(self, url, sleept_time=1):
        """
        Open any URL in the web browser

        Args:
            url (str): URL to open
            sleept_time (int, optional): Time to wait for the page to load correctly. Defaults to 1.
        """        
        self.driver.get(url)
        self.current_url = url
        sleep(sleept_time)

    def get_html_content(self):
        """
        Return HTML content of current page

        Returns:
            str: HTML page
        """        
        return self.driver.page_source

    """
    TODO:
    Any method that can be wrapped.
    For example:
    Click button by id. 
    """    