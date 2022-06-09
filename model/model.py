import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib as plt

tf.random.set_seed(42)
np.random.seed(42)

#print out some info
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.experimental.list_physical_devices('CPU')))

#get the data
training_input = pd.read_csv('bond_types.csv')
training_output = pd.read_csv('energy.csv')

#make the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(8, activation = 'relu'))
model.add(tf.keras.layers.Dense(1))

model.compile(optimizer="SGD", loss="mse", metrics="mae")

#run and save the model
model.fit(training_input, training_output, epochs = 2)
model.save('model')

