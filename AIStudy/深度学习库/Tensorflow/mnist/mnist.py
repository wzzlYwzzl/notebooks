from tensorflow import keras
import numpy as np
import os,sys

def load_data(path='mnist.npz'):
  """Loads the MNIST dataset.
  """
  cwd = sys.path[0]
  path = os.path.join(cwd, path)
  
  with np.load(path) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

    return (x_train, y_train), (x_test, y_test)

#这个加载数据的方法是目前最新的tensorflow支持的方式
#keras.datasets.mnist.load_data()
(x_train, y_train), (x_test, y_test) = load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0

model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(28,28)))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test,y_test)