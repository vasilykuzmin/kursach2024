import sys
sys.path.append('../')

from dataset import dataset_cache

from splitted_data import SplittedData
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from IPython.display import clear_output
from deepmerge import always_merger
import tempfile

class Model:
    def __init__(self, net):
        self.net = net
        self.description = {}
    
    def addDescription(self, description):
        always_merger.merge(self.description, description)

    def loadDataset(self, description: dict, preprocessor, test_split=0.1, val_split=0.1) -> None:
        '''Loads dataset from file and preprocesses it.'''
        raw_dataset = dataset_cache.get(description)
        preprocessed_dataset = preprocessor.preprocessDataset(raw_dataset)
        self.dataset = SplittedData(preprocessed_dataset, test_split, val_split)

    def fit(self, optimizer, loss_function, batch_size=1024, epochs=10):
        losses = []
        try:
            for epoch in tqdm(range(epochs)):
                # train
                for batch_start in tqdm(range(0, self.dataset.trainX.shape[0], batch_size)):
                    optimizer.zero_grad()
                    y = self.net(torch.from_numpy(self.dataset.trainX[batch_start:min(batch_start + batch_size, self.dataset.trainX.shape[0])]))
                    loss = loss_function(y, torch.from_numpy(self.dataset.trainY))
                    loss.backward()
                    optimizer.step()

                # test
                y = self.net(torch.from_numpy(self.dataset.testX))
                losses.append(loss_function(y, torch.from_numpy(self.dataset.testY)).item())

                clear_output(True)
                plt.figure(figsize=(6, 4))
                plt.plot(losses)
                plt.title('Loss')
                plt.ylabel('Loss')
                plt.xlabel('epoch')
                plt.grid()

                plt.show()

        except KeyboardInterrupt:
            print('Keyboard interrupt.')

        self.addDescription({'model': {'metrics': {'Loss': losses}}})
        torch.set_printoptions(profile="full")
        self.addDescription({'model': {'weights': str(self.net.state_dict())}})
        self.addDescription({'min_loss': min(losses)})

    def getDescription(self):
        return self.description
