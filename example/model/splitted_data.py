import numpy as np


class SplittedData():
    def __init__(self, data: np.ndarray, test_split: float, val_split: float) -> None:
        self.X, self.Y = data

        train_split = 1 - test_split - val_split

        numTrainX = int(self.X.shape[0] * train_split)
        numTrainY = int(self.Y.shape[0] * train_split)
        numTestX = self.X.shape[0] - int(self.X.shape[0] * test_split)
        numTestY = self.Y.shape[0] - int(self.Y.shape[0] * test_split)

        self.trainX = self.X[:numTrainX]
        self.trainY = self.Y[:numTrainY]
        self.valX = self.X[numTrainX:numTestX]
        self.valY = self.Y[numTrainY:numTestY]
        self.testX = self.X[numTestX:]
        self.testY = self.Y[numTestY:]

    @property
    def getTrainX(self):
        return self.trainX
    
    @property
    def getTrainY(self):
        return self.trainY
    
    @property
    def getValX(self):
        return self.valX
    
    @property
    def getValY(self):
        return self.valY
    
    @property
    def getTestX(self):
        return self.testX
    
    @property
    def getTestY(self):
        return self.testY
    