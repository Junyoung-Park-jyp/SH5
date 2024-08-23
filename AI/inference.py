import os
import torch
import sys

import pandas as pd
import numpy as np
from tqdm import tqdm

from transformers import TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer

from modules.metrics import compute_metrics
from modules.trainer import CustomTrainer
from modules.utils import load_yaml
from modules.preprocess import preprocess_infer
from modules.dataset import CustomDataset

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Root directory
PROJECT_DIR = os.path.dirname(__file__)

# Load config
config_path = os.path.join(PROJECT_DIR, 'config', 'inference_config.yaml')
config = load_yaml(config_path)

# Recorder directory
CHECKPOINT_DIR = os.path.join(PROJECT_DIR, 'results', config.TEST.CHECKPOINT_PATH)
OUTPUT_DIR = os.path.join(CHECKPOINT_DIR, 'test_results')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data directory
DATA_DIR = os.path.join(PROJECT_DIR, 'data', config.TEST.DIRECTORY.dataset)

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def test():
    output_dir = OUTPUT_DIR
    pretrained_link = config.MODEL.pretrained_link[config.MODEL.model_name]
    num_of_classes = config.MODEL.num_of_classes
    max_seq_len = config.MODEL.max_seq_len
    checkpoint_path = CHECKPOINT_DIR
    
    test_args = TrainingArguments(
        output_dir=output_dir,
        per_device_eval_batch_size=256,
        # report_to = 'wandb',
        dataloader_pin_memory=False,
        do_eval=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path, num_labels = num_of_classes).to(device)

    data = pd.read_csv(DATA_DIR + '_test.csv', index_col = 0)
    data = preprocess_infer(data)
    dataset = CustomDataset(data, pretrained_link, max_seq_len)

    # wandb.login()

    trainer = CustomTrainer(
        model=model,
        args=test_args,
        compute_metrics=compute_metrics,
        eval_dataset=dataset
    )
    trainer.evaluate()


def inference(data):
    output_dir = OUTPUT_DIR
    pretrained_link = config.MODEL.pretrained_link[config.MODEL.model_name]
    num_of_classes = config.MODEL.num_of_classes
    max_seq_len = config.MODEL.max_seq_len
    checkpoint_path = CHECKPOINT_DIR
    
    print('=' * 50)
    print('Get Model & Tokenizer')
    print('=' * 50)

    test_args = TrainingArguments(
        output_dir=output_dir,
        dataloader_pin_memory=False,
        do_predict=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path, num_labels=num_of_classes).to(device)
    trainer = CustomTrainer(
        model=model,
        args=test_args,
        compute_metrics=compute_metrics,
    )

    tokenizer = AutoTokenizer.from_pretrained(pretrained_link)

    print('=' * 50)
    print('Tokenizing...')
    print('=' * 50)

    items = list()

    if type(data) == str:
        item = {key: torch.tensor(val).to(device) for key, val in tokenizer(data,
                                                                            truncation=True,
                                                                            padding='max_length',
                                                                            max_length=max_seq_len).items()}
        items.append(item)

    elif type(data) == pd.DataFrame:
        for name in tqdm(data['업체명_r']):
            item = {key: torch.tensor(val).to(device) for key, val in tokenizer(name, 
                                                                                truncation=True,
                                                                                padding='max_length',
                                                                                max_length=max_seq_len).items()}
            items.append(item)

    print('=' * 50)
    print('Predicting...')
    print('=' * 50)

    test_results = trainer.predict(items)
    label_ids = np.argmax(test_results[0], axis=1)

    if type(data) == str:
        return config.LABELING[label_ids[0]]

    elif type(data) == pd.DataFrame:
        data['업종'] = label_ids
        data['업종'] = data['업종'].replace(config.LABELING.keys(), config.LABELING.values())
        return data


if __name__ == '__main__':
    import time

    # Test
    # print(test())

    # DataFrame
    # result = inference(preprocess_infer(pd.read_csv('data/uncased_test.csv', index_col=0)))
    # result.to_csv('inferenced.csv')

    # Keyword
    start = time.time()
    input_text = '피자스쿨'
    output_text = inference(preprocess_infer(input_text))
    print(f'Input: {input_text}, Output: {output_text} Inference Time: {time.time() - start}')
