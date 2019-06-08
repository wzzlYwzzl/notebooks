[TOC]

# 几种基于梯度的优化方法可视化对比

## 1. Long Valley

Algos without scaling based on gradient information really struggle to break symmetry here - SGD gets no where and Nesterov Accelerated Gradient / Momentum exhibits oscillations until they build up velocity in the optimization direction.

Algos that scale step size based on the gradient quickly break symmetry and begin descent.

![longValley](./images/1.gif)

## 2. Beale's function

Due to the large initial gradient, velocity based techniques shoot off and bounce around - adagrad almost goes unstable for the same reason.

Algos that scale gradients/step sizes like adadelta and RMSProp proceed more like accelerated SGD and handle large gradients with more stability.

![longValley](./images/2.gif)

## 3. Saddle Point

Behavior around a saddle point.

NAG/Momentum again like to explore around, almost taking a different path. 

Adadelta/Adagrad/RMSProp proceed like accelerated SGD.

![longValley](./images/3.gif)
