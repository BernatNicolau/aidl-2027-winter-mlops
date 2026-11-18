import pandas as pd
import torch


class MyDataset(torch.utils.data.Dataset):

    def __init__(self, images_path: str, labels_path: str):
        super().__init__()
        self.images_path = images_path
        self.labels_path = labels_path
        self.data = pd.read_csv(self.images_path)
        self.labels = pd.read_csv(self.labels_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data.iloc[idx], self.labels.iloc[idx]