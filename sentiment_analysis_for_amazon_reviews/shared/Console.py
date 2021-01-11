#!/usr/bin/env python
import argparse
import logging
from sentiment_analysis_for_amazon_reviews.shared.inference import Inference
from sentiment_analysis_for_amazon_reviews.shared.test_model import Test_Model
from sentiment_analysis_for_amazon_reviews.shared.trainer import Trainer
class Console(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None
    
    def argumentParse(self):
        self.parser.add_argument("--cli", help="Modo consola",action="store_true",default=False)
        self.parser.add_argument("--ws", help="Modo Web Service",action="store_true",default=False)
        self.parser.add_argument("--eval-model", help="Evaluar modelo",action="store_true",default=False)
        self.parser.add_argument("--inference", help="Inferir",action="store_true",default=False)
        self.parser.add_argument("--train", help="entrenar",action="store_true",default=False)
        self.parser.add_argument('--host','-H',nargs='?',type=str,default='0.0.0.0',help='recibe el host con el cual estara escuchando el servidor, 0.0.0.0 para todas las ip')
        self.parser.add_argument('--port','-P',nargs='?',type=int,default=8001,help='Recibe el puerto en el cual estara escuchado el servidor')
        self.parser.add_argument('--debug',default=True, action="store_true", help='modo debug')
        self.args = self.parser.parse_args()
    
    def iniciar(self):
        self.argumentParse()
        if self.args.eval_model:
            test_model = Test_Model()
            test_model.evaluar_modelo()
        elif self.args.inference:
            inference = Inference()
            inference.inference()
        elif self.args.train:
            trainer = Trainer()
            trainer.entrenar()
        print(self.args)
