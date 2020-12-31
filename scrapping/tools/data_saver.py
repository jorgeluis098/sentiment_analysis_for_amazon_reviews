from pandas import DataFrame,concat
from os import path
from datetime import datetime

from scrapping.common.singleton import singleton

@singleton
class DataSaver(object):
    def __init__(self):
        super().__init__()
        department_path = path.join("scrapping_data","department","data_"+self.get_current_timestamp()+".csv")
        self.department_df = PandasSave(department_path)
        category_path = path.join("scrapping_data","category","data_"+self.get_current_timestamp()+".csv")
        self.category_df = PandasSave(category_path)
        product_category_path = path.join("scrapping_data","product_category","data_"+self.get_current_timestamp()+".csv")
        self.product_category_df = PandasSave(product_category_path)
        product_page_path = path.join("scrapping_data","product_page","data_"+self.get_current_timestamp()+".csv")
        self.product_page_df = PandasSave(product_page_path)
        product_path = path.join("scrapping_data","product","data_"+self.get_current_timestamp()+".csv")
        self.product_df = PandasSave(product_path)
        product_path = path.join("scrapping_data","review","data_"+self.get_current_timestamp()+".csv")
        self.review_df = PandasSave(product_path,columns=["review","stars"])       

    def product_append(self, name, link):
        self.product_df.append(name, link)
    
    def review_append(self, review, stars):
        self.review_df.append(review, stars)

    def department_append(self, name, link):
        self.department_df.append(name, link)

    def category_append(self, name, link):
        self.category_df.append(name, link)

    def product_category_append(self, name, link):
        self.product_category_df.append(name, link)

    def product_page_append(self, name, link):
        self.product_page_df.append(name, link)

    def save_department(self):
        self.department_df.save_dataframe()

    def save_category(self):
        self.category_df.save_dataframe()

    def save_product_category(self):
        self.product_category_df.save_dataframe()
         
    def save_product_page(self):
        self.product_page_df.save_dataframe()


    def get_current_timestamp(self):
        return str(datetime.timestamp(datetime.now()))
        

class PandasSave(object):

    def __init__(self, path, columns=['Name', 'link']):
        super().__init__()
        self.columns = columns
        self.df = DataFrame(columns=self.columns)
        self.path = path
        self.names = []
        self.links = []

    def gen_dataframe(self, data):
        return DataFrame([data], columns=self.columns)

    def append(self, *args):
        self.df = concat([self.df,  self.gen_dataframe([field for field in args])])
        if (self.df.shape[0] % 10) == 0:
            self.save_dataframe()
        return

    def save_dataframe(self):
        self.df.to_csv(self.path)
        return


