import pandas as pd
from dataset.data_loader import getPeriodData
import pickle
import gzip
import hashlib
import os

default_description = ['filename', 'symbol', 'interval', 'startTime', 'endTime', 'croppedColumnsNames']

def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def processDescription(description: dict) -> None:
    '''Adds missing fields in dictionary'''
    for field in default_description:
        if not field in description:
            description[field] = None
    description['dataLoaderHash'] = md5(f'{os.path.dirname(__file__)}/data_loader.py')
    description['datasetCacheHash'] = md5(f'{os.path.dirname(__file__)}/dataset_cache.py')

def download(description: dict) -> None:
    '''Downloads dataset with these parameters.'''
    processDescription(description)

    data = getPeriodData(description['symbol'], 
                         description['interval'], 
                         description['startTime'], 
                         description['endTime'], 
                         description['croppedColumnsNames'],)
    os.makedirs(os.path.dirname(description["filename"]), exist_ok=True)
    with gzip.open(description["filename"], 'wb') as f:
        pickle.dump((data, description), f)

def load(filename: str) -> pd.DataFrame:
    '''Loads dataset from storage.'''
    with gzip.open(filename, 'rb') as f:
        data, description = pickle.load(f)
    return data.astype('float64'), description

def check(description: dict) -> bool:
    '''Checks if there is valid dataset.'''
    processDescription(description)

    try:
        data, data_description = load(description['filename'])
    except FileNotFoundError:
        return False
    return description == data_description

def get(description: dict) -> pd.DataFrame:
    '''Load dataset. If there is no valid downloads one.'''
    processDescription(description)
    if check(description):
        return load(description['filename'])[0]
    download(description)
    if check(description):
        return load(description['filename'])[0]
    raise Exception('Cannot download dataset.')
