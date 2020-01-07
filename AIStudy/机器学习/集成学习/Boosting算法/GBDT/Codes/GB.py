"""
参考：
scikit-learn 梯度提升树(GBDT)调参小结
https://www.cnblogs.com/DjangoBlog/p/6201663.html
"""

import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingClassifier
from sklearn import model_selection, metrics
from sklearn.model_selection import GridSearchCV

import matplotlib.pylab as plt

"""加载数据
"""
train = pd.read_csv('/Users/caoxiaojie/train_modified.csv')
target = 'Disbursed'
IDcol = 'ID'
#print(train[target].value_counts())

x_columns = [x for x in train.columns if x not in [target, IDcol]]
#print(x_columns)
X = train[x_columns]
y = train[target]

"""使用默认参数
"""
def test_0(X,y):
    gbm = GradientBoostingClassifier(random_state=10)
    gbm.fit(X,y)

    y_pred = gbm.predict(X)
    y_predprob = gbm.predict_proba(X)[:,1]

    print("Accuracy:{}".format(metrics.accuracy_score(y.values, y_pred)))
    print("AUC Score:{}".format(metrics.roc_auc_score(y, y_predprob)))
    
    """ 
        Accuracy : 0.9852
        AUC Score (Train): 0.900531
    """
#test_0(X,y)

"""
首先对learning_rate和n_estimators调参：
"""

def search_param_0(X,y):
    param = {'n_estimators':range(20,81,10)}
    g_search = GridSearchCV(estimator=GradientBoostingClassifier(
        learning_rate=0.1,
        min_samples_split=300,
        min_samples_leaf=20,
        max_depth=8,
        max_features='sqrt',
        subsample=0.8,
        random_state=10
    ), param_grid=param, scoring='roc_auc', iid=False, cv=5)
    g_search.fit(X,y)
    
    print(g_search.cv_results_['mean_test_score'],g_search.cv_results_['params'])
    print(g_search.best_params_)
    print(g_search.best_score_)

    """
    [0.81284735 0.81437929 0.81403709 0.81592869 0.81926607 0.81721608
    0.81485328] [{'n_estimators': 20}, {'n_estimators': 30}, {'n_estimators': 40}, {'n_estimators': 50}, {'n_estimators': 60}, {'n_estimators': 70}, {'n_estimators': 80}]
    {'n_estimators': 60}
    0.8192660696138212
    """

#search_param_0(X,y)

"""
对决策树的最大深度max_depth和划分所需最小样本数min_samples_split。
"""

def search_param_1(X,y):
    params = {
        'max_depth':range(3,14,2),
        'min_samples_split':range(100,801,200)
    }
    
    g_search = GridSearchCV(
        estimator=GradientBoostingClassifier(
            learning_rate=0.1,
            n_estimators=60,
            min_samples_leaf=20,
            max_features='sqrt',
            subsample=0.8,
            random_state=10
        ),
        param_grid=params,
        scoring='roc_auc',
        iid=False,
        cv=5
    )
    g_search.fit(X,y)
    print(g_search.cv_results_['mean_test_score'],g_search.cv_results_['params'])
    print(g_search.best_params_)
    print(g_search.best_score_)