from binance.spot import Spot
import pandas as pd
from tqdm import tqdm


defaultCroppedColumnsNames = ['Open time', 'Close time', 'Open', 'Close', 'High', 'Low', 'Volume']
rawColumnsNames = [
    'Open time',
    'Open', 
    'High', 
    'Low', 
    'Close', 
    'Volume', 
    'Close time',
    'Quote asset volume',
    'Number of trades',
    'Taker buy base asset volume',
    'Taker buy quote asset volume',
    'Ignore',
    ]


def getRawBatch(client, symbol, interval, startTime=None, endTime=None, limit=None):
    return pd.DataFrame(client.klines(symbol, interval, startTime=startTime, endTime=endTime, limit=limit), dtype='float64', columns=rawColumnsNames)


def getBatchCloseTime(batch):
    return int(batch.loc[batch.shape[0] - 1, 'Close time'])


def getPeriodData(symbol, interval, startTime, endTime=None, croppedColumnsNames=None):
    batchSize = 1000
    client = Spot()

    if endTime == None:
        endTime = getBatchCloseTime(getRawBatch(client, symbol, interval, limit=1))
    if croppedColumnsNames == None:
        croppedColumnsNames = defaultCroppedColumnsNames

    data = pd.DataFrame(columns=croppedColumnsNames)
    localTime = startTime
    
    with tqdm(total=(endTime - startTime + 1)) as pbar:
        while localTime < endTime:
            batch = getRawBatch(client, symbol, interval, localTime, endTime=endTime, limit=batchSize)
            croppedBatch = batch.loc[:, croppedColumnsNames]
            data = pd.concat([data, croppedBatch], ignore_index=True)

            nextTime = getBatchCloseTime(batch) + 1
            pbar.update(nextTime - localTime)
            localTime = nextTime
    return data


def getPeriodDataToCSV(filename, symbol, interval, startTime, endTime=None, croppedColumnsNames=None):
    data = getPeriodData(symbol, interval, startTime, endTime=endTime, croppedColumnsNames=croppedColumnsNames)
    data.to_csv(filename)
