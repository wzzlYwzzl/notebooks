"""这里的代码是和TimeDistributed.md文件相关的。
"""
#%%
"""我们接下来都假设解决的问题是：给定如下序列：[0,0.2,0.4,0.6,0.8]，
然后输出序列是：[0,0.2,0.4,0.6,0.8]
"""
from numpy import array
length = 5
seq = array([i/float(length) for i in range(length)])
print(seq)

#%%
"""one-to-one LSTM
把上面的序列预测问题变成了如下的一个X,y
X, y
0   0
0.2 0.2
0.4 0.4
0.6 0.6
0.8 0.8
"""

# 构建模型的代码
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# prepare sequence
length = 5
seq = array([i/float(length) for i in range(length)])

# 由于Keras中使用LSTM，要求输入X必须是3D的数据，所以先做如下变换
X = seq.reshape(len(seq), 1, 1)
y = seq.reshape(len(seq), 1)

# define LSTM configuration
n_neurons = length
n_batch = length
n_epoch = 1000

# create LSTM
model = Sequential()
model.add(LSTM(n_neurons, input_shape=(1, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())
# train LSTM
#model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)
# evaluate
#result = model.predict(X, batch_size=n_batch, verbose=0)
#for value in result:
#    print('%.1f' % value)

"""
lstm参数数量计算：4是门数量
n = 4 * ((inputs + 1) * outputs + outputs^2)
n = 4 * ((1 + 1) * 5 + 5^2)
n = 4 * 35
n = 140
"""

#%%
"""many-to-one
这里没有通过TimeDistributed来实现。
"""
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# prepare sequence
length = 5
seq = array([i/float(length) for i in range(length)])
X = seq.reshape(1, length, 1)
y = seq.reshape(1, length)
# define LSTM configuration
n_neurons = length
n_batch = 1
n_epoch = 500
# create LSTM
model = Sequential()
model.add(LSTM(n_neurons, input_shape=(length, 1)))
model.add(Dense(length)) #many to one，为啥这里不是one呢？

model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())
# train LSTM
model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)
# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)
for value in result[0,:]:
    print(value)

#%%
"""Many-to-many
这里通过TimeDistributed来实现。
"""
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import LSTM
# prepare sequence
length = 5
seq = array([i/float(length) for i in range(length)])
X = seq.reshape(1, length, 1)
y = seq.reshape(1, length, 1)
# define LSTM configuration
n_neurons = length
n_batch = 1
n_epoch = 1000
# create LSTM
model = Sequential()
model.add(LSTM(n_neurons, input_shape=(length, 1), return_sequences=True))
model.add(TimeDistributed(Dense(1)))
model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())
# train LSTM
model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)
# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)
for value in result[0,:,0]:
	print(value)