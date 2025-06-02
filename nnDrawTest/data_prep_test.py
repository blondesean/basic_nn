import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./dataset/symbol_data.csv')
print(df.head())

# Check max and min pixel value (ignore Label column)
pixels = df.iloc[:, 1:].values
print('Max pixel:', pixels.max())
print('Min pixel:', pixels.min())

# Plot first sample as 28x28 image (if 28x28 pixels = 784)
img = pixels[0].reshape(28, 28)
plt.imshow(img, cmap='gray')
plt.show()
