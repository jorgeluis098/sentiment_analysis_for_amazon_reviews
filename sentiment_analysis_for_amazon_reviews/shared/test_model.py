import torch
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification, BertModel, AutoConfig
import numpy as np
import pandas as pd
from os import path
from tqdm import tqdm
from sentiment_analysis_for_amazon_reviews.classifier.data_load import Data

class Test_Model():
    def __init__(self):
        self.device = 'cuda' if cuda.is_available() else 'cpu'

    def calcuate_accu(self, big_idx, targets):
        n_correct = (big_idx==targets).sum().item()
        return n_correct

    def test(self):
        tr_loss = 0
        n_correct = 0
        nb_tr_steps = 0
        nb_tr_examples = 0
        # Iteramos sobre el set de datos de testing
        for _,data in tqdm(enumerate(testing_loader, 0)):
            ids = data['ids'].to(self.device, dtype = torch.long)
            mask = data['mask'].to(self.device, dtype = torch.long)
            targets = data['targets'].to(self.device, dtype = torch.long)
            # Pasamos los datos a la red
            outputs = model(ids, mask)
            loss = loss_function(outputs, targets)
            tr_loss += loss.item()
            big_val, big_idx = torch.max(outputs.data, dim=1)
            n_correct += self.calcuate_accu(big_idx, targets)
            nb_tr_steps += 1
            nb_tr_examples+=targets.size(0)
        print(f"-------")
        epoch_loss = tr_loss/nb_tr_steps
        epoch_accu = (n_correct*100)/nb_tr_examples
        print(f"Testing loss: {epoch_loss}")
        print(f"Testing Accuracy: {epoch_accu}")

    def evaluar_modelo(self):
        data_path = path.join("scrapping_data","final", "final_dataset_balanced.csv")
        df = pd.read_csv(data_path)

        train_size = 0.8
        train_dataset=df.sample(frac=train_size,random_state=200)
        test_dataset=df.drop(train_dataset.index).reset_index(drop=True)

        model_file = path.join("models","sentimentanalysis.bin")
        model_dir = path.join("models")

        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        loss_function = torch.nn.CrossEntropyLoss()

        modelo=torch.load(model_file)
        modelo.to(self.device)

        testing_set = Data(test_dataset, tokenizer, 512)

        test_params = {'batch_size': 2,
                        'shuffle': True,
                        'num_workers': 0
                        }

        testing_loader = DataLoader(testing_set, **test_params)
        modelo.eval()
        self.test()
