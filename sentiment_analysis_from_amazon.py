# -*- coding: utf-8 -*-
"""Sentiment Analysis From Amazon

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HCfeldoQTKIiSMDvBukpJ_s7AVS5lrBz

#**Sentiment Analysis From Amazon México using BERT**

#### Este Colab es para clasificar sentimientos usando BERT con un conjunto de datos minados en reseñas de Amazon México.

Istalamos los módulos que necesitamos para crear nuestra red, dado que ya se encuentran instalados los módulos de pandas y pytorch no es necesario instalarlos.
#### Importamos los módulos a usar



*   **Torch**: Para implementar nuestar red neuronal
*   **transformers**: Contiene ya implementados varias arquitecturas basadas en transformers, de aqui vamos a obtener BERT.
*   **numpy**: Para operaciones matemáticas varias.
*   **pandas**: Para leer los datos almacenados en un .csv

Se establece el dispositivo a usar, si esta disponible una gpu, la utilizará, en caso contrario se usará el CPU.


"""

import torch
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification, BertModel, AutoConfig
import numpy as np
import pandas as pd
from os import path

device = 'cuda' if cuda.is_available() else 'cpu'
print(device)
torch.set_grad_enabled(False)

"""### **Preparación de los datos**

#### Se declaran los hiperparámetros del modelo y el modelo pre entrenado.
"""

MODEL_NAME = "dccuchile/bert-base-spanish-wwm-uncased"
# Definimos los hiperparámetros del modelo
MAX_LEN = 512
TRAIN_BATCH_SIZE = 2
VALID_BATCH_SIZE = 1
LEARNING_RATE = 1e-05
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

"""#### Se cargan los datos, en este caso estan en la carpeta raiz."""
data_path = path.join("scrapping_data","final", "final_dataset_balanced.csv")
df = pd.read_csv(data_path)
print(df['sentiment'].value_counts(normalize=True))
print(df['sentiment'].value_counts())
df.head()

def print_tokens(text):
  input = tokenizer(
    text,
    return_tensors="pt"
  )
  print("Tokens (int)      : {}".format(input['input_ids'].tolist()[0]))
  print("Tokens (str)      : {}".format([tokenizer.convert_ids_to_tokens(s) for s in input['input_ids'].tolist()[0]]))
  print("Tokens (attn_mask): {}".format(input['attention_mask'].tolist()[0]))
  print()

print_tokens("al querer cargar el raton la entrada o ranura")

"""#### Se crea una clase donde vamos a tener todos los datos, cada vez que se quiera acceder a un item, pasará por __getitem__ donde regresará los ids en forma de tensor, la máscara y el "target" que es la clase que queremos determinar."""

class Data(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len
        
    def __getitem__(self, index):
        review = str(self.data.review[index])
        review = " ".join(review.split())
        inputs = self.tokenizer.encode_plus(
            review,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            pad_to_max_length=True,
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'targets': torch.tensor(self.data.sentiment[index], dtype=torch.long)
        } 
    
    def __len__(self):
        return self.len

"""#### Creamos los datasets's de entrenamiento y de test. Para ello usamos el 80% del dataset para entrenamiento."""

train_size = 0.8
train_dataset=df.sample(frac=train_size,random_state=200)
test_dataset=df.drop(train_dataset.index).reset_index(drop=True)
train_dataset = train_dataset.reset_index(drop=True)

print("FULL Dataset: {}".format(df.shape))
print("TRAIN Dataset: {}".format(train_dataset.shape))
print("TEST Dataset: {}".format(test_dataset.shape))

training_set = Data(train_dataset, tokenizer, MAX_LEN)
testing_set = Data(test_dataset, tokenizer, MAX_LEN)

"""#### Creamos los objetos DataLoader, que van a ser importantes para el entrenamiento y test.

Definimos los parámetros de entrenamiento como el batch_size, "barajeamos" los datos para hacerlos random y definimos el número de workers, en este caso decidimos dejar que el main thread se encargue de eso.
"""

train_params = {'batch_size': TRAIN_BATCH_SIZE,
                'shuffle': True,
                'num_workers': 0
                }

test_params = {'batch_size': VALID_BATCH_SIZE,
                'shuffle': True,
                'num_workers': 0
                }

training_loader = DataLoader(training_set, **train_params)
testing_loader = DataLoader(testing_set, **test_params)

"""### **Definición de la Red**

#### **Constructor**
Heredamos la clase torch.nn.Module para definir nuestra red neuronal.

1.- Definimos la primera capa como el modelo BERT completo. 

2.- Lo pasamos pro un pre clasificador lineal

3.- Definimos el clasificador final a dos categorias

4.- Definimos un dropout para evitar el overfitting.

#### **Forward**
En este método se define el comportamiento que va a tener la red, con las capas definidas anteriormente, vamos pasando la información de una capa a otra con o sin funciones de activación.

1.- Recibimos los ids y el attention mask, de el dataset.

2.- Pasamos los datos a la primera capa (BERT)

3.- Recuperamos el tensor que contiene la información necesaria.

4.- Lo pasamos por el preclasificador

5.- Le aplicamos una ReLu como función de activación

6.- Desacrtivamos algunos nodos con dropout para el overfitting

7.- Lo pasamos por el clasificador y regresamos el resultado
"""

class Classifier(torch.nn.Module):
    def __init__(self, MODEL_NAME):
        super(Classifier, self).__init__()
        self.l1 =BertModel.from_pretrained(MODEL_NAME)
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.classifier = torch.nn.Linear(768, 2)
        self.dropout = torch.nn.Dropout(0.3)
        

    def forward(self, input_ids, attention_mask):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output

"""#### Pasamos creamos el modelo y lo pasamos al dispositivo (cpu o gpu)"""

model = Classifier(MODEL_NAME)
model.to(device)

"""#### Definimos la función de pérdida, en este caso usamos cross entropy, ya que es muy útil para problemas de clasificación.

#### Ademas, definimos el optimizador.
"""

loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params =  model.parameters(), lr=LEARNING_RATE)

"""#### Generamos una función para calcular la exactitud del modelo"""

def calcuate_accu(big_idx, targets):
    n_correct = (big_idx==targets).sum().item()
    return n_correct

"""### Entrenamiento

Definimos una funcipon para imprimir en consola datos sobre el entrenamiento
"""

def print_info(epoch, n_correct, nb_tr_examples, tr_loss, nb_tr_steps):
  print(f"-------")
  print(f'The Total Accuracy for Epoch {epoch}: {(n_correct*100)/nb_tr_examples}')
  epoch_loss = tr_loss/nb_tr_steps
  epoch_accu = (n_correct*100)/nb_tr_examples
  print(f"Training Loss Epoch: {epoch_loss}")
  print(f"Training Accuracy Epoch: {epoch_accu}")

"""#### Definimos la función train donde pasamos los datos, optimizamos la red y generamos datos de entrenamiento."""

loss_=[]
acc_=[]
def train(epoch):
    tr_loss = 0
    n_correct = 0
    nb_tr_steps = 0
    nb_tr_examples = 0
    model.train()
    # Iteramos sobre el set de entrenamiento
    for _,data in enumerate(training_loader, 0):
        # Pasamos los datos al dispositivo y con una precisión dada por long.
        ids = data['ids'].to(device, dtype = torch.long)
        mask = data['mask'].to(device, dtype = torch.long)
        targets = data['targets'].to(device, dtype = torch.long)
        # Pasamos ids y mask al modelo
        outputs = model(ids, mask)
        # Calculamos la pérdida
        loss = loss_function(outputs, targets)
        # La guardamos para hacer un análisis posterior
        loss_.append(loss.item())
        tr_loss += loss.item()
        # Calculamos la exactitud o accuracy del modelo
        big_val, big_idx = torch.max(outputs.data, dim=1)
        n_correct += calcuate_accu(big_idx, targets)
        # Aumentamos los pasos de entrenamiento, nuevamente para realizar 
        # un análisis del comportamiento del modelo en el entrenamiento
        nb_tr_steps += 1
        nb_tr_examples+=targets.size(0)
        # Cada 100 pasos muestra la información del entrenamiento
        if _%100==0:
            loss_step = tr_loss/nb_tr_steps
            accu_step = (n_correct*100)/nb_tr_examples 
            print(f"Training Loss per 100 steps: {loss_step}")
            print(f"Training Accuracy per 100 steps: {accu_step}")
            acc_.append(accu_step)
            loss_.append(loss_step)
        optimizer.zero_grad()
        loss.backward()
        # # When using GPU
        optimizer.step()
        print_info(epoch, n_correct, nb_tr_examples, tr_loss, nb_tr_steps)
    return

"""#### Hora de entrenar !!!!!!"""

torch.set_grad_enabled(True)
EPOCHS=5
for epoch in range(EPOCHS):
    print("Epoca:", epoch)
    train(epoch)

"""#### Graficamos el comportamiento del entrenamiento"""
from datetime import datetime
from os import path

timestamp = str(datetime.timestamp(datetime.now())).replace(".","_")
data_path = path.join("graphics","loss_"+timestamp+".csv")
step = list(range(len(loss_)))
loss_df = pd.DataFrame()
loss_df["step"] = step
loss_df["loss"] = loss_
loss_df.to_csv(data_path,index=False)

data_path = path.join("graphics","acc_"+timestamp+".csv")
step = list(range(len(acc_)))
acc_df = pd.DataFrame()
acc_df["step"] = step
acc_df["accuracy"] = acc_
acc_df.to_csv(data_path,index=False)
"""### Test de la Red

#### Definimos la función de test
"""

def test():
    tr_loss = 0
    n_correct = 0
    nb_tr_steps = 0
    nb_tr_examples = 0
    # Iteramos sobre el set de datos de testing
    for _,data in enumerate(testing_loader, 0):
        ids = data['ids'].to(device, dtype = torch.long)
        mask = data['mask'].to(device, dtype = torch.long)
        targets = data['targets'].to(device, dtype = torch.long)
        # Pasamos los datos a la red
        outputs = model(ids, mask)
        loss = loss_function(outputs, targets)
        #loss.grad_fn=True
        tr_loss += loss.item()
        big_val, big_idx = torch.max(outputs.data, dim=1)
        n_correct += calcuate_accu(big_idx, targets)

        nb_tr_steps += 1
        nb_tr_examples+=targets.size(0)
    print(f"-------")
    epoch_loss = tr_loss/nb_tr_steps
    epoch_accu = (n_correct*100)/nb_tr_examples
    print(f"Testing loss: {epoch_loss}")
    print(f"Testing Accuracy: {epoch_accu}")

    return

"""#### Aplicamos el test"""

model.eval()
test()

"""### Guardamos el modelo entrenado"""

output_model_file = path.join("models","sentimentanalysis.bin")
output_dir = path.join("models")
#output_model_file = '/content/model/sentimentanalysis.bin'
#output_dir = '/content/model/'

model_to_save = model
torch.save(model_to_save, output_model_file)
tokenizer.save_pretrained(output_dir)
config_file = AutoConfig.from_pretrained(MODEL_NAME)
config_file.save_pretrained(output_dir)

print('All files saved')

"""### Cargamos el modelo entrenado para hacer inferencia"""

model_file = path.join("models","sentimentanalysis.bin")
model_dir = path.join("models")

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model=torch.load(model_file)
model.to(device)

def inference_text(text, tokenizer, model):
  review = " ".join(text.lower().split())
  inputs = tokenizer.encode_plus(
      review,
      None,
      add_special_tokens=True,
      max_length=512,
      pad_to_max_length=True,
      return_token_type_ids=True,
      truncation=True
  )
  ids = inputs['input_ids']
  mask = inputs['attention_mask']

  ids = torch.tensor(ids, dtype=torch.long)
  mask = torch.tensor(mask, dtype=torch.long)
  data_set = [{
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
        }]
  params = {'batch_size': 1,
                  'num_workers': 0
                  }
  loader = DataLoader(data_set, **params)
  for _,data in enumerate(loader, 0):
    ids = data['ids'].to(device, dtype = torch.long)
    mask = data['mask'].to(device, dtype = torch.long)
    output = model(ids, mask)
  big_val, big_idx = torch.max(output.data, dim=1)
  return int(big_idx[0].int())

text = "Es muy inestable , hubiese preferido pagar mas por algo mejor"
model.eval()
inference_text(text,tokenizer, model)