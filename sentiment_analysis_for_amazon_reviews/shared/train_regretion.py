import pandas as pd
import numpy as np
from os import path
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from threading import Thread
from sentiment_analysis_for_amazon_reviews.shared.Logger import Logger
import matplotlib.pyplot as plt
logger = Logger()
logging = logger.get_logger()
class Train_Regretion():
    def __init__(self):
        self.data_path = path.join("scrapping_data","final", "final_dataset_balanced.csv")
        self.df = pd.read_csv(self.data_path)
        self.data = pd.DataFrame(columns=['word', 'sentiment'])

    def humanize_token(self, token):
        return token.replace("(","").replace(",", "").replace(".","").replace(")","")

    def get_tokens_sentiment(self, review, sentiment):
        datas = []
        for r in review:
            datas.append([self.humanize_token(r) ,sentiment])
        datasFrame = pd.DataFrame(datas, columns=['word', 'sentiment'])
        self.data = self.data.append(datasFrame, ignore_index=True)
        logging.info("Fin de hilo para crear DataSet")

    def generar_dataSet_palabra_sentimiento(self):
        for index,t in tr.df.iterrows():
            logging.info("iniciado hilo para crear DataSet: {}".format(index))
            try:
                tr.get_tokens_sentiment(t['review'], t['sentiment'])
            except:
                pass
        self.data.to_csv(path.join("scrapping_data","final", "final_dataset_balanced_word_lineal.csv"), index=False)
    
    def generar_estadisticas_palabras(self):
        path_words = path.join("scrapping_data","final", "final_dataset_balanced_word_lineal.csv")
        df = pd.read_csv(path_words)
        dictos = {}
        for index,t in df.iterrows():
            key = "{}-{}".format(str(t['word']).replace("-",""), t['sentiment'])
            if key in dictos.keys():
                dictos[key] += 1
            else:
                dictos[key] = 1
        datas = []
        for di in dictos.keys():
            di_s = di.split("-")
            datas.append([di_s[0],di_s[1], dictos[di]])
        data_frame = pd.DataFrame(datas, columns=['word', 'sentiment', 'count'])
        data_frame.to_csv(path.join("scrapping_data","final", "final_dataset_balanced_word_lineal_count.csv"), index=False)
    
    def generar_modelo_regresion_lineal(self):
        path_words = path.join("scrapping_data","final", "final_dataset_balanced_word_lineal_count.csv")
        df = pd.read_csv(path_words)
        x_train = df[["sentiment"]]
        y_train = df["count"]
        colores=['orange','blue']
        regr = linear_model.LinearRegression()
        regr.fit(x_train, y_train)
        y_pred = regr.predict(x_train)
        print(y_pred)
        asignar=[]
        for index, row in df.iterrows():
            if(row['sentiment']==0):
                asignar.append(colores[0])
            else:
                asignar.append(colores[1])
        plt.scatter(x_train, y_train, c=asignar)
        plt.plot(x_train,y_pred)
        plt.show()
        

    
if __name__ == "__main__":
    tr = Train_Regretion()
    #tr.generar_dataSet_palabra_sentimiento()
    #tr.generar_estadisticas_palabras()
    tr.generar_modelo_regresion_lineal()
