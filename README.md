# Sentiment Analysis For Amazon Reviews

Sentiment Analysis For Amazon Reviews is a Finetuned Neural Network based on BERT for amazon reviews in spanish. These reviews are from Amazon México.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Anaconda Install

Use anaconda [anaconda](https://www.anaconda.com/) to install.

```bash
conda env create --name envname --file=sentimentanalysis.yml
```
Activate Enviroment.

```bash
conda activate envname
```
## Scrapping
If you want to run the scraping, you must have the [Mozilla Firefox](https://www.mozilla.org/es-ES/firefox/) browser installed.

If you want to do the complete scraping, in the main file add the code:

```python
from scrapping.request_scrapping import AmazonSacrapping
scrapper = AmazonSacrapping()
scrapper.get_all_categories()
```
## Train Model
If you want to train the model, for now xD must configure the BATCH_SIZE, for training, corresponding to the memory capacity of the GPU or RAM. And for now run the following command.
```bash
python sentiment_analysis_from_amazon.py
```

## Inference
For now, if you want to test the inference, you have to modify the inference.py file, modify the part of the text and execute.
For example:
```python
text = "Es muy inestable , hubiese preferido pagar mas por algo mejor"
model.eval()
sentiment_class = inference_text(text,tokenizer, model)
print(sentiment_class)
```
```bash
python inference.py
```

## Usage

```bash
python main.py 
```

## pip usage
```bash
pip install .
```
## Console usage
```
usage: sentiment-analysis-for-amazon-reviews [-h] [--cli] [--ws] [--eval-model] [--inference]
                                             [--train] [--host [HOST]] [--port [PORT]]
                                             [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --cli                 Modo consola
  --ws                  Modo Web Service
  --eval-model          Evaluar modelo
  --inference           Inferir
  --train               entrenar
  --host [HOST], -H [HOST]
                        recibe el host con el cual estara escuchando el servidor, 0.0.0.0
                        para todas las ip
  --port [PORT], -P [PORT]
                        Recibe el puerto en el cual estara escuchado el servidor
  --debug               modo debug

``` 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
