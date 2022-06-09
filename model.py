import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

tf.random.set_seed(42)
np.random.seed(42)

#print out some info
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.experimental.list_physical_devices('CPU')))

#get the data
u = pd.read_csv('./data/processed/bond_types.csv')
y = pd.read_csv('./data/processed/energy.csv')
#split into training and testing
u_train, u_validate, y_train, y_validate = train_test_split(u, y, test_size=.2, shuffle=True, random_state=42)

#make the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(8, activation = 'relu'))
model.add(tf.keras.layers.Dense(1))

model.compile(optimizer="SGD", loss="mse", metrics="mae")

#run and save the model
model.fit(u_train, y_train, epochs = 2)
model.save('model')

