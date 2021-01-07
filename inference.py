import torch
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoTokenizer
import pandas as pd
from os import path

from classifier.model import Classifier

device = 'cuda' if cuda.is_available() else 'cpu'

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
      padding='longest',
      return_token_type_ids=True,
      truncation=True
  )
  ids = inputs['input_ids']
  mask = inputs['attention_mask']

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
sentiment_class = inference_text(text,tokenizer, model)
print(sentiment_class)