"""代码例子来自：https://www.jianshu.com/p/719fc024c0ec
"""

from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier as GBDT
from sklearn.ensemble import ExtraTreesClassifier as ET
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.ensemble import AdaBoostClassifier as ADA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np

"""准备数据
"""
x,y = make_classification(n_samples=6000)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5)

"""定义第一层：第一层模型尽量选择选择表达能力强的，这样才能保证后面模型能够获取足够的信息
"""
clfs = [ GBDT(n_estimators=100),
       RF(n_estimators=100),
       ET(n_estimators=100),
       ADA(n_estimators=100)
]
X_train_stack  = np.zeros((X_train.shape[0], len(clfs)))
X_test_stack = np.zeros((X_test.shape[0], len(clfs))) 

"""6折交叉验证，同时通过第一层的强模型训练预测生成喂给第二层的特征数据。
"""
### 6折stacking
n_folds = 6
skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=1)
for i,clf in enumerate(clfs):
#     print("分类器：{}".format(clf))
    X_stack_test_n = np.zeros((X_test.shape[0], n_folds))
    for j,(train_index,test_index) in enumerate(skf.split(X_train,y_train)):
                tr_x = X_train[train_index]
                tr_y = y_train[train_index]
                clf.fit(tr_x, tr_y)
                #生成stacking训练数据集
                X_train_stack [test_index, i] = clf.predict_proba(X_train[test_index])[:,1]
                X_stack_test_n[:,j] = clf.predict_proba(X_test)[:,1]
    #生成stacking测试数据集
    X_test_stack[:,i] = X_stack_test_n.mean(axis=1)

"""为了防止过拟合，第二层选择了一个简单的Logistics回归模型。输出Stacking模型的auc得分
"""
clf_second = LogisticRegression(solver="lbfgs")
clf_second.fit(X_train_stack,y_train)
pred = clf_second.predict_proba(X_test_stack)[:,1]
score = roc_auc_score(y_test,pred)#0.9946
print(score)

# GBDT分类器
clf_1 = clfs[0]
clf_1.fit(X_train,y_train)
pred_1 = clf_1.predict_proba(X_test)[:,1]
score = roc_auc_score(y_test,pred_1)#0.9922
print(score)

# 随机森林分类器
clf_2 = clfs[1]
clf_2.fit(X_train,y_train)
pred_2 = clf_2.predict_proba(X_test)[:,1]
score = roc_auc_score(y_test,pred_2)#0.9944
print(score)

# ExtraTrees分类器
clf_3 = clfs[2]
clf_3.fit(X_train,y_train)
pred_3 = clf_3.predict_proba(X_test)[:,1]
score = roc_auc_score(y_test,pred_3)#0.9930
print(score)

# AdaBoost分类器
clf_4 = clfs[3]
clf_4.fit(X_train,y_train)
pred_4 = clf_4.predict_proba(X_test)[:,1]
score = roc_auc_score(y_test,pred_4)#0.9875
print(score)