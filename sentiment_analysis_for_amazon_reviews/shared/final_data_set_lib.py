from sentiment_analysis_for_amazon_reviews.scrapping.request_scrapping import AmazonSacrapping
from os import path,listdir
from pandas import read_csv,DataFrame,concat
import emoji
from sklearn.utils import resample
# Update yml file
# conda env export > sentiment_analysis.yml

def get_reviews_from_product_pages():
    data_path = path.join("scrapping_data","product_page","data.csv")
    i = -1
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
    final_name = "final_reviews.csv"
    final_data = DataFrame()
    for csv in listdir(data_path):
        df = read_csv(path.join(data_path,csv))
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.drop_duplicates(subset ="review", keep = False, inplace = True) 
        final_data = concat([final_data,df])
    final_data = final_data.loc[:, ~final_data.columns.str.contains('^Unnamed')]
    print(final_data.head())
    final_data.to_csv(path.join(data_path,final_name), index=False)

def give_emoji_free_text(text):
    allchars = [strg for strg in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([strg for strg in text.split() if not any(i in strg for i in emoji_list)])
    return clean_text

def create_separated_datasets():
    data_path = path.join("scrapping_data","review","final_reviews.csv")
    negative_path= path.join("scrapping_data","review","negative.csv")
    positive_path = path.join("scrapping_data","review","positive.csv")
    df = read_csv(data_path)
    # Convert Uncased reviews
    df["review"] = df['review'].str.lower()
    # Remove emojis
    df["review"] = df['review'].apply(lambda x : give_emoji_free_text(str(x))) 
    print(df.groupby(["stars"]).count())
    #Negative_dataset
    negative_df = df[(df["stars"] == 1) | (df["stars"]==2)]
    negative_df["sentiment"] = 0
    negative_df.to_csv(negative_path, index=False)
    #Positive_dataset
    positive_df = df[(df["stars"] == 4) | (df["stars"]==5)]
    positive_df["sentiment"] = 1
    positive_df.to_csv(positive_path, index=False)

def resample_df(df):
    df_positive = df[df.sentiment==1]
    df_negative = df[df.sentiment==0]
    if df_positive.shape[0]>df_negative.shape[0]:
        df_minority = df_negative
        df_majority = df_positive
    else:
        df_minority = df_positive
        df_majority = df_negative
    df_majority_sampled = resample(df_majority, 
                                    replace=True,
                                    n_samples=df_minority.shape[0],
                                    random_state=123) 
    return concat([df_minority, df_majority_sampled])


def concatenate_final_dataset(filename="final_dataset.csv" ,balance_data=False):
    data_path = path.join("scrapping_data","final")
    final_data = DataFrame()
    for csv in listdir(data_path):
        df = read_csv(path.join(data_path,csv))
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.drop_duplicates(subset ="review", keep = False, inplace = True) 
        final_data = concat([final_data,df])
    final_data = final_data.loc[:, ~final_data.columns.str.contains('^Unnamed')]
    if balance_data:
        final_data = resample_df(final_data)
    print(final_data.head())
    final_data.to_csv(path.join(data_path,filename), index=False)

def create_final_dataset():
    concatenate_final_dataset(filename="final_dataset_balanced.csv", balance_data=True)
    concatenate_final_dataset(filename="final_dataset_unbalanced.csv")
