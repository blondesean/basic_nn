# model.py
import torch.nn as nn

class SymbolClassifier(nn.Module):
    def __init__(self, input_size=28*28, num_classes=18):
        super(SymbolClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        return self.net(x)

