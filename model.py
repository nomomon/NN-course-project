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
bond_types = pd.read_csv('./data/processed/bond_types.csv').to_numpy()
no_of_atoms = pd.read_csv('./data/processed/atom_counts.csv').to_numpy()
u = np.concatenate([bond_types, no_of_atoms], axis=1)
y = pd.read_csv('./data/processed/energy.csv').to_numpy()
#split into training and testing
u_train, _, y_train, _ = train_test_split(u, y, test_size=.2, shuffle=True, random_state=42)

#make the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(8, activation = 'relu'))
model.add(tf.keras.layers.Dense(1))

model.compile(optimizer="Adam", loss="mse", metrics="mae")

#save training logs
callback = tf.keras.callbacks.CSVLogger('training_logs_Adam_with_noAtoms.csv')

#save best model
best_model_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath = 'best_model_Adam_with_noAtoms',
    monitor='val_loss',
    save_best_only=True,
    save_weights_only=False,
    mode='min'
)

no_epochs = 300

#run and save the model
model.fit(u_train, y_train, epochs = no_epochs, validation_split=.2, callbacks=[callback])
model.save('model_Adam_with_noAtoms')

