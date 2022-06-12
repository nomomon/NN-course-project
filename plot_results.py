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
bond_types = pd.read_csv('./data/processed/bond_types.csv').to_numpy()
no_of_atoms = pd.read_csv('./data/processed/atom_counts.csv').to_numpy()
u = np.concatenate([bond_types, no_of_atoms], axis=1)
y = pd.read_csv('./data/processed/energy.csv').to_numpy()
#split into training and testing
_, u_validate, _, y_validate = train_test_split(u, y, test_size=.2, shuffle=True, random_state=42)

model = tf.keras.models.load_model('model_Adam_with_noAtoms')

print(model.evaluate(u_validate, y_validate))

df = pd.read_csv('training_logs_Adam_with_noAtoms.csv')
df.plot(
    x = 'epoch',
    y = ['loss', 'val_loss']
)

df.plot(
    x = 'epoch',
    y = ['mae', 'val_mae']
)

plt.show()