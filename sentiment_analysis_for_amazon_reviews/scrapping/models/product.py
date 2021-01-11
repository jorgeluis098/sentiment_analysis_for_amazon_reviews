from sentiment_analysis_for_amazon_reviews.scrapping.tools.firefox_selenium import FirefoxScrapping
from selenium.common.exceptions import NoSuchElementException
from sentiment_analysis_for_amazon_reviews.scrapping.tools.data_saver import DataSaver
from sentiment_analysis_for_amazon_reviews.scrapping.models.review import Review


class Product(object):
    def __init__(self, name, url_base, href, save_data=True):
        super().__init__()
        self.name = name
        self.url_base = url_base
        self.href = href
        try:
            self.reviews = self.get_review_s()
            self.create_reviews()
            if save_data:
                self.data_saver = DataSaver()
                self.save_object()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            pass

            
    def get_url(self):
        return self.url_base + self.href

    def save_object(self):
        self.data_saver.product_append(self.name,self.url_base + self.href)

    def create_reviews(self):
        self.elements = []
        for review in self.reviews:
            self.elements.append(Review(review[0],review[1]))


    def get_review_s(self):
        from selenium import webdriver
        # from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.keys import Keys
        import time
        my_list2 = []
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = FirefoxScrapping().driver
        driver.get(self.get_url())
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
            # for i in range(len(my_list2)):
            #     print(i, my_list2[i],"\n\n")
            return my_list2
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
                # for i in range(len(my_list2)):
                #     print(i, my_list2[i],"\n\n")
                return my_list2
                driver.close()
            except NoSuchElementException as exception:
                print("NO REVIEW xD")
        return []