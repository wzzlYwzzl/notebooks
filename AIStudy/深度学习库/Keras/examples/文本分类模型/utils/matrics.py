# -*- coding: utf-8 -*-

import numpy as np
from sklearn.metrics import accuracy_score


def eval_acc(y_true, y_pred):
    y_true = np.argmax(y_true, axis=-1)
    y_pred = np.argmax(y_pred, axis=-1)

    acc = accuracy_score(y_true, y_pred)
    return acc
