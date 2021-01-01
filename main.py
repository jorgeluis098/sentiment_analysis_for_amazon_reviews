from scrapping.request_scrapping import AmazonSacrapping
from os import path,listdir
from pandas import read_csv,DataFrame,concat

def get_reviews_from_product_pages():
    data_path = path.join("scrapping_data","product_page","data.csv")
    i = 3
    scrapper = AmazonSacrapping()
    product_pages = scrapper.load_product_page(data_path, id_partition=i, partition=4)
    products = []
    bandera = False
    for page in product_pages:
        products_page = page.get_products()
        if products_page:
            products += products_page

def create_final_file():
    data_path = path.join("scrapping_data","review")
    final_name = "final_reviews_mals.csv"
    final_data = DataFrame()
    for csv in listdir(data_path):
        df = read_csv(path.join(data_path,csv), index_col=0)
        df.drop_duplicates(subset ="review", keep = False, inplace = True) 
        final_data = concat([final_data,df])
    final_data.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    print(final_data.head())
    final_data.to_csv(path.join(data_path,final_name), index=False)

create_final_file()


