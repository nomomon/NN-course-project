import matplotlib.pyplot as plt
from tensorflow import keras

#load the model (including its history)
model = keras.models.load_model('model')

#plot the results
plt.plot(model.history['mae'])
plt.title('model loss')
plt.ylabel('mae')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()