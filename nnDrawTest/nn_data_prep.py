# dataset.py
import torch
from torch.utils.data import Dataset
import pandas as pd

class SymbolDataset(Dataset):
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        self.labels = df.iloc[:, 0].astype('category')
        self.label_ids = self.labels.cat.codes
        self.data = df.iloc[:, 1:].values / 255.0  # normalize

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = torch.tensor(self.data[idx], dtype=torch.float32)
        y = torch.tensor(self.label_ids[idx], dtype=torch.long)
        return x, y
