import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from os import path
import platform

class FirefoxScrapping(object):
    def __init__(self):
        super().__init__()
        self.url_base="https://www.amazon.com.mx/"
        self.set_driver()
        self.driver.get(self.url_base)

    def set_driver(self):
        os_info = platform.system()
        webdriver_filename=""
        if platform.system() == "Windows":
            firefox_webdriver_filename="geckodriver.exe"
        elif platform.system() == "Linux":
            firefox_webdriver_filename="geckodriver"
<<<<<<< HEAD
        # firefox_webdriver_path=path.join("webdriver",firefox_webdriver_filename)
        firefox_webdriver_path = path.join("scrapping","tools","webdriver",firefox_webdriver_filename)
=======
        #firefox_webdriver_path = path.join("scrapping","tools","webdriver",firefox_webdriver_filename)
        firefox_webdriver_path=path.join("webdriver",firefox_webdriver_filename)
>>>>>>> 2f8fa54fb0743008a074502ac0c5383fff8943f6
        self.driver = webdriver.Firefox(executable_path=firefox_webdriver_path)
    
    def get_all_categories(self):
        url = self.url_base + "gp/site-directory?ref_=nav_em__allcategories_0_1_1_30"
        self.driver.get(url)
        table = self.driver.find_element_by_id("shopAllLinks")
        