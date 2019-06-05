import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def sigmoid(x):
    """sigmoid函数
    
    Arguments:
        x {narray} -- 输入向量
    
    Returns:
        narray -- 对每个元素球sigmoid
    """
    return 1 / (1 + np.exp(-x))


def load_data(file):
    """从文件中加载数据
    
    Arguments:
        file {str} -- 文件名称
    
    Returns:
        narray,narray -- 数据和标签
    """
    data_matrix = []
    data_label = []

    f = open(file, mode='r',encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        fields = line.strip().split()
        if len(fields) == 3:
            #注意这里把wx+b处理为xw，所以添加了1
            data_matrix.append([1, float(fields[0]), float(fields[1])])
            data_label.append(int(fields[2]))

    print(data_matrix)
    print(data_label)

    data = np.mat(data_matrix)
    label = np.mat(data_label).transpose()

    return data, label


def gradient_ascent(data, label):
    """梯度上升法，每个迭代都是用所有的数据
    """
    m,n = np.shape(data)
    w = np.ones((n,1))

    alpha = 0.001
    num = 500

    for i in range(500):
        err = sigmoid(data*w) - label
        #print(err)
        #这里w-***，对比公式即可明白
        w = w - alpha * data.transpose() * err

    return w


def draw(weight,data_file):
    """绘制图像
    """
    x0List=[]
    y0List=[]
    x1List=[]
    y1List=[]
    f=open(data_file,'r')
    for line in f.readlines():
        lineList=line.strip().split()
        if lineList[2]=='0':
            x0List.append(float(lineList[0]))
            y0List.append(float(lineList[1]))
        else:
            x1List.append(float(lineList[0]))
            y1List.append(float(lineList[1]))

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(x0List,y0List,s=10,c='red')
    ax.scatter(x1List,y1List,s=10,c='green')

    xList=[];yList=[]
    x=np.arange(-3,3,0.1)
    for i in np.arange(len(x)):
        xList.append(x[i])

    y=(-weight[0]-weight[1]*x)/weight[2]
    for j in np.arange(y.shape[1]):
        yList.append(y[0,j])

    ax.plot(xList,yList)
    plt.xlabel('x1');plt.ylabel('x2')
    plt.show()

if __name__ == '__main__':
    file = 'data.txt'
    file = os.path.join(sys.path[0], file)
    data,label = load_data(file)
    weight = gradient_ascent(data, label)
    draw(weight, file)