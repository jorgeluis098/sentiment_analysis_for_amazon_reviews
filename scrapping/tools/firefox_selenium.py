import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from os import path
import platform
from time import sleep

from scrapping.common.singleton import singleton

@singleton
class FirefoxScrapping(object):
    def __init__(self):
        self.set_driver()

    def set_driver(self):
        os_info = platform.system()
        firefox_webdriver_filename=""
        if platform.system() == "Windows":
            firefox_webdriver_filename="geckodriver.exe"
        elif platform.system() == "Linux":
            firefox_webdriver_filename="geckodriver"
        firefox_webdriver_path=path.join("scrapping","tools","webdriver",firefox_webdriver_filename)
        self.driver = webdriver.Firefox(executable_path=firefox_webdriver_path)
    
    def open_url(self, url, sleept_time=1):
        self.driver.get(url)
        sleep(sleept_time)

    def get_html_content(self):
        return self.driver.page_source