from tensorflow import keras

#这个加载数据的方法是目前最新的tensorflow支持的方式
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()