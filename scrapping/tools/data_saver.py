from pandas import DataFrame,concat
from os import path

from scrapping.common.singleton import singleton

@singleton
class DataSaver(object):
    def __init__(self):
        super().__init__()
        department_path = path.join("scrapping_data","department","data.csv")
        self.department_df = PandasSave(department_path)
        category_path = path.join("scrapping_data","category","data.csv")
        self.category_df = PandasSave(category_path)
        product_category_path = path.join("scrapping_data","product_category","data.csv")
        self.product_category_df = PandasSave(product_category_path)
        product_page_path = path.join("scrapping_data","product_page","data.csv")
        self.product_page_df = PandasSave(product_page_path)

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
        

class PandasSave(object):

    def __init__(self, path):
        super().__init__()
        self.columns = ['Name', 'link']
        self.df = DataFrame(columns=self.columns)
        self.path = path
        self.names = []
        self.links = []

    def gen_dataframe(self, name, link):
        return DataFrame([[name,link]], columns=self.columns)

    def append(self, name, link):
        self.df = concat([self.df,  self.gen_dataframe(name, link)])
        if (self.df.shape[0] % 10) == 0:
            self.save_dataframe()
        return

    def save_dataframe(self):
        self.df.to_csv(self.path)
        return


