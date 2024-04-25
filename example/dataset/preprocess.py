import numpy as np
import pandas as pd
from dataset.features import MACD, RSI, ROC, TSI


class Preprocessor:
    def __init__(self, klines_number, columns_number) -> None:
        super().__init__()
        self.klines_number = klines_number
        self.columns_number = columns_number
        self.omax = 0
        self.omin = 0
        self.numberOfFeatures = 0

    @staticmethod
    def normalize(data: np.ndarray) -> np.ndarray:
        data -= data.max(axis=0) - (data.max(axis=0) - data.min(axis=0)) / 2
        return data / data.max(axis=0)

    @staticmethod
    def cut(x: np.ndarray, y: np.ndarray):
        size = min(x.shape[0], y.shape[0])
        x = x[-size:]
        y = y[-size:]
        return x, y

    def addFeature(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        self.numberOfFeatures += 1
        y = self.normalize(y)
        y = np.expand_dims(y, 1)
        x, y = self.cut(x, y)
        x = np.concatenate([x, y], axis=1)
        return x

    def unnormalize(self, data: np.ndarray):
        #shape must be [, columns_number]
        oldnmax = (self.omax - self.omin) / 2
        return data * oldnmax + self.omax - oldnmax

    def unnormalizeX(self, X):
        #shape must be [, columns_number * klines_number + numberOfFeatures]
        omax = (np.tile(self.omax, [self.klines_number]))
        omin = (np.tile(self.omin, [self.klines_number]))
        omax = np.insert(omax, omax.shape[0], [1] * self.numberOfFeatures)
        omin = np.insert(omin, omin.shape[0], [1] * self.numberOfFeatures)
        oldnmax = (omax - omin) / 2
        return X * oldnmax + omax - oldnmax

    def addFeatures(self, X: np.ndarray, rawDataset: np.ndarray) -> np.ndarray:
        X = self.addFeature(X, MACD(rawDataset[:-1, 3], 13, 26, 9))
        X = self.addFeature(X, RSI(rawDataset[:-1, 3], 13))
        X = self.addFeature(X, RSI(rawDataset[:-1, 3], 26))
        X = self.addFeature(X, ROC(rawDataset[:-1, 3], 13))
        X = self.addFeature(X, ROC(rawDataset[:-1, 3], 26))
        X = self.addFeature(X, TSI(rawDataset[:-1, 3], 13, 13))
        X = self.addFeature(X, TSI(rawDataset[:-1, 3], 26, 26))
        return X

    def preprocessDataset(self, _rawDataset: pd.DataFrame):
        rawDataset = _rawDataset.loc[:, 'Close time':].to_numpy()

        self.omax = rawDataset.max(axis=0)
        self.omin = rawDataset.min(axis=0)
        rawDataset = self.normalize(data=rawDataset)

        X = np.lib.stride_tricks.sliding_window_view(rawDataset, self.klines_number, axis=0)
        dX = X[:, 3, self.klines_number - 1] - X[:, 3, self.klines_number - 2]
        Y = np.where(dX < 0, -1.0, 1.0)[1:]
        X = X.reshape(X.shape[0], self.klines_number * self.columns_number)[:-1, :]

        # X = self.addFeatures(X=X, rawDataset=rawDataset)
        X, Y = self.cut(X, Y)
        return X, Y
