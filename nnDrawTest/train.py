
# train.py
import torch
from torch.utils.data import DataLoader, random_split
from symbol_classifier import SymbolClassifier
from nn_data_prep import SymbolDataset
import torch.nn as nn
import torch.optim as optim

BATCH_SIZE = 32
EPOCHS = 10
CSV_PATH = "./dataset/symbol_data.csv"

dataset = SymbolDataset(CSV_PATH)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_ds, val_ds = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SymbolClassifier().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# Save the model
torch.save(model.state_dict(), "symbol_model.pt")
