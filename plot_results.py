import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

tf.random.set_seed(42)
np.random.seed(42)

#print out some info
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.experimental.list_physical_devices('CPU')))

#get the data
u = pd.read_csv('./data/processed/bond_types.csv').to_numpy()
y = pd.read_csv('./data/processed/energy.csv').to_numpy()
#split into training and testing
_, u_validate, _, y_validate = train_test_split(u, y, test_size=.2, shuffle=True, random_state=42)

model = tf.keras.models.load_model('model_SGD')

print(model.evaluate(u_validate, y_validate))

df = pd.read_csv('training_logs_SGD.csv')
df.plot(
    x = 'epoch',
    y = ['loss', 'val_loss']
)

df.plot(
    x = 'epoch',
    y = ['mae', 'val_mae']
)

plt.show()