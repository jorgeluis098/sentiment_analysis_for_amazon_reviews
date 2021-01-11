import torch
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification, BertModel, AutoConfig
import numpy as np
import pandas as pd
from os import path
from sentiment_analysis_for_amazon_reviews.classifier.data_load import Data
from sentiment_analysis_for_amazon_reviews.classifier import Classifier
from sentiment_analysis_for_amazon_reviews.shared.Logger import Logger
logger = Logger()
logging = logger.get_logger()

class Trainer():
    def __init__(self):
        self.device = 'cuda' if cuda.is_available() else 'cpu'
        torch.set_grad_enabled(False)
        self.MODEL_NAME = "dccuchile/bert-base-spanish-wwm-uncased"
        # Definimos los hiperparámetros del modelo
        self.MAX_LEN = 512
        self.TRAIN_BATCH_SIZE = 2
        self.VALID_BATCH_SIZE = 1
        self.EPOCHS = 5
        LEARNING_RATE = 1e-05
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.data_path = path.join("scrapping_data","final", "final_dataset_balanced.csv")
        self.df = pd.read_csv(self.data_path)
        self.df.head()
        self.model = Classifier(self.MODEL_NAME)
        self.model.to(self.device)
        self.loss_function = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(params =  self.model.parameters(), lr=LEARNING_RATE)
        self.loss_=[]
        self.acc_=[]
        self.train_size = 0.8
        self.train_dataset = self.df.sample(frac=self.train_size, random_state=200)
        self.test_dataset = self.df.drop(self.train_dataset.index).reset_index(drop=True)
        self.train_dataset = self.train_dataset.reset_index(drop=True)
        self.train_params = {'batch_size': self.TRAIN_BATCH_SIZE,
                'shuffle': True,
                'num_workers': 0
                }

        self.test_params = {'batch_size': self.VALID_BATCH_SIZE,
                'shuffle': True,
                'num_workers': 0
                }

        self.training_set = Data(self.train_dataset, self.tokenizer, self.MAX_LEN)
        self.testing_set = Data(self.test_dataset, self.tokenizer, self.MAX_LEN)

        self.training_loader = DataLoader(self.training_set, **self.train_params)
        self.testing_loader = DataLoader(self.testing_set, **self.test_params)
        self.output_model_file = path.join("models","sentimentanalysis.bin")
        self.output_dir = path.join("models")
        
    
    def print_tokens(self, text):
        input = self.tokenizer(
            text,
            return_tensors="pt"
        )
        logging.info("Tokens (int)      : {}".format(input['input_ids'].tolist()[0]))
        logging.info("Tokens (str)      : {}".format([self.tokenizer.convert_ids_to_tokens(s) for s in input['input_ids'].tolist()[0]]))
        logging.info("Tokens (attn_mask): {}".format(input['attention_mask'].tolist()[0]))


    def print_info(self, epoch, n_correct, nb_tr_examples, tr_loss, nb_tr_steps):
        logging.debug(f'paso {nb_tr_steps}')
        logging.info(f'The Total Accuracy for Epoch {epoch}: {(n_correct*100)/nb_tr_examples}')
        epoch_loss = tr_loss/nb_tr_steps
        epoch_accu = (n_correct*100)/nb_tr_examples
        logging.info(f"Training Loss Epoch: {epoch_loss}")
        logging.info(f"Training Accuracy Epoch: {epoch_accu}")
    
    def calcuate_accu(self, big_idx, targets):
        n_correct = (big_idx==targets).sum().item()
        return n_correct
    
    def train(self, epoch):
        tr_loss = 0
        n_correct = 0
        nb_tr_steps = 0
        nb_tr_examples = 0
        self.model.train()
        # Iteramos sobre el set de entrenamiento
        for _,data in enumerate(self.training_loader, 0):
            # Pasamos los datos al dispositivo y con una precisión dada por long.
            ids = data['ids'].to(self.device, dtype = torch.long)
            mask = data['mask'].to(self.device, dtype = torch.long)
            targets = data['targets'].to(self.device, dtype = torch.long)
            # Pasamos ids y mask al modelo
            outputs = self.model(ids, mask)
            # Calculamos la pérdida
            loss = self.loss_function(outputs, targets)
            # La guardamos para hacer un análisis posterior
            self.loss_.append(loss.item())
            tr_loss += loss.item()
            # Calculamos la exactitud o accuracy del modelo
            big_val, big_idx = torch.max(outputs.data, dim=1)
            n_correct += self.calcuate_accu(big_idx, targets)
            # Aumentamos los pasos de entrenamiento, nuevamente para realizar 
            # un análisis del comportamiento del modelo en el entrenamiento
            nb_tr_steps += 1
            nb_tr_examples += targets.size(0)
            # Cada 100 pasos muestra la información del entrenamiento
            if _%100==0:
                loss_step = tr_loss/nb_tr_steps
                accu_step = (n_correct*100)/nb_tr_examples 
                logging.info(f"Training Loss per 100 steps: {loss_step}")
                logging.info(f"Training Accuracy per 100 steps: {accu_step}")
                self.acc_.append(accu_step)
                self.loss_.append(loss_step)
            self.optimizer.zero_grad()
            loss.backward()
            # # When using GPU
            self.optimizer.step()
            self.print_info(epoch, n_correct, nb_tr_examples, tr_loss, nb_tr_steps)
        return

    def entrenar(self):
        torch.set_grad_enabled(True)
        for epoch in range(self.EPOCHS):
            logging.info("Epoca: {}".format(epoch))
            self.train(epoch)
        self.guardar()
    
    def guardar(self):
        model_to_save = self.model
        torch.save(model_to_save, self.output_model_file)
        self.tokenizer.save_pretrained(self.output_dir)
        config_file = AutoConfig.from_pretrained(self.MODEL_NAME)
        config_file.save_pretrained(self.output_dir)
        logging.info('Archivos guardados correctamente')
