import torch
import io
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoTokenizer
import pandas as pd
from os import path
from sentiment_analysis_for_amazon_reviews.classifier import Classifier

class Inference():
  def __init__(self):
    print(__name__)
    self.device = 'cuda' if cuda.is_available() else 'cpu'
    self.model_file = path.join("models","sentimentanalysis.bin")
    with open(self.model_file, 'rb') as f:
      buffer = io.BytesIO(f.read())
    self.modelo = torch.load(buffer)
    self.modelo.to(self.device)
    

  def inference_text(self, text, tokenizer, model):
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
      ids = data['ids'].to(self.device, dtype = torch.long)
      mask = data['mask'].to(self.device, dtype = torch.long)
      output = model(ids, mask)
    big_val, big_idx = torch.max(output.data, dim=1)
    return int(big_idx[0].int())

  def inference(self):

    model_dir = path.join("models")

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    

    text = "Es muy inestable , hubiese preferido pagar mas por algo mejor"
    self.modelo.eval()
    sentiment_class = self.inference_text(text,tokenizer, self.modelo)
    print(sentiment_class)
