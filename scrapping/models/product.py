# from scrapping.tools.firefox_selenium import FirefoxScrapping
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException

class Product(object):
    def __init__(self, url_prod):
        self.url_prod = url_prod
        # super().__init__()


    def get_review_s(self):
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.keys import Keys
        import time
        my_list2 = []
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url_prod)
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="reviews-medley-global-expand-head"]/div[2]/div/span/a').click()
        except:
            # print("SOLO EN ESPAÑOL O SIN COMENTARIOS")
            pass
        try:
            # hace click en mostrar todos los comentarios
            driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div[2]/a').click()
            time.sleep(2)
            
            for i in range(1,13):
                try:
                    temp=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span').text                                              
                    # my_list2.append(driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span').text)
                    # import pdb;pdb.set_trace()
                    try:
                        stars=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[2]/a[1]/i').get_attribute("textContent")
                        stars2=int(float(stars.split()[0]))
                        my_list2.append((temp,stars2))
                    except:
                        my_list2.append((temp,"-1"))
                    # my_list2.append(temp)
                    print("elemento en español")
                    # import pdb;pdb.set_trace() 
                    if temp=='':
                        my_list2.pop()
                        print("elemento vacio en lista de reviews")
                        temp=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span[2]').text
                        stars=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[2]/i').get_attribute("textContent")
                        stars2=int(float(stars.split()[0]))                                
                        my_list2.append((temp,stars2))
                        # my_list2.append(temp)
                    # my_list2.append(driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span'))
                except:
                    print("Excepción fin")
            for i in range(len(my_list2)):
                print(i, my_list2[i],"\n\n")
            driver.close()

        except NoSuchElementException as exception:
            try:
                print("\nEsta en ingles!!\n")
                # hace click en mostrar todos los comentarios
                button = driver.find_element_by_xpath('//*[@id="cr-pagination-footer-0"]/a')
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                for i in range(4,16):
                    try:
                        temp=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span[2]').text
                        stars=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[2]/i').get_attribute("textContent")
                        # my_list2.append(driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[{i}]/div/div/div[4]/span/span[2]').text)
                        stars2=int(float(stars.split()[0]))
                        my_list2.append((temp,stars2))
                        if temp=='':
                            my_list2.pop()
                            # print("elemento vacio en lista de reviews")
                    except:
                        pass
                for i in range(len(my_list2)):
                    print(i, my_list2[i],"\n\n")
                driver.close()
            except NoSuchElementException as exception:
                print("NO REVIEW xD")


# algo = Product('http://www.amazon.com.mx/Mario-Kart-Deluxe-Nintendo-Standard/dp/B01N1037CV/ref=lp_21558445011_1_1')
algo = Product('https://www.amazon.com.mx/William-Shakespeares-Empire-Striketh-Back/dp/1594747156/ref=sr_1_5?dchild=1&qid=1609302794&s=books&sr=1-5')
# algo = Product('https://www.amazon.com.mx/Fellowes-CRC34008-crc34008-cross-cut-Refurbished-Shredder/dp/B017OA8TKQ/ref=lp_17596115011_1_6')
# algo = Product('https://www.amazon.com.mx/Canon-Angular-9520B002-reacondicionado-Certificado/dp/B01L5K43I8/ref=lp_17596115011_1_5')
# algo = Product('https://www.amazon.com.mx/Sony-Dualshock-Wireless-Controller-PlayStation/dp/B07VQVG4GS/ref=pd_rhf_dp_s_pd_crcbs_1_6/141-7724177-1612006?_encoding=UTF8&pd_rd_i=B07VQVG4GS&pd_rd_r=94a8d38d-e713-41d1-8800-a5ec431fc7f5&pd_rd_w=HNKqU&pd_rd_wg=oqYbl&pf_rd_p=2f0d13e7-1e39-406c-85d4-06f91668892b&pf_rd_r=D129NZ5M50ATRDEQ8K9S&refRID=D129NZ5M50ATRDEQ8K9S&th=1')
# algo = Product('https://www.amazon.com.mx/SuperSonic-TV-7-SC-195-Renewed/dp/B07N8423S2/ref=lp_17596115011_1_2?th=1')
# algo = Product('https://www.amazon.com.mx/Inal%C3%A1mbrica-Bluetooth-Subwoofer-Reacondicionado-Certificado/dp/B07DW9NG35/ref=lp_17596115011_1_1')
algo.get_review_s()