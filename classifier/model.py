import torch
from transformers import BertModel

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