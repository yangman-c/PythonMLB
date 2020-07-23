from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import  train_test_split
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

cancer = load_breast_cancer()
print("cancer.keys():\n{}".format(cancer.keys()))
print("Shape of cancer data:{}".format(cancer.data.shape))
print("Sample counts per class:\n{}".format({n:v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
print("Feature names:\n{}".format(cancer.feature_names))

X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target, random_state=66)
traning_accuracy = []
test_accuracy = []
# n_neighbors取值从1到10
neighbors_settings = range(1, 11)

for n_neighbors in neighbors_settings:
    #构建模型
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    #记录训练集精度
    traning_accuracy.append(clf.score(X_train, y_train))
    #记录繁华精度
    test_accuracy.append(clf.score(X_test, y_test))

plt.plot(neighbors_settings, traning_accuracy, label="traing_accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel(":Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.show()

# http://yunhq.sse.com.cn:32041//v1/sh1/line/000001?begin=0&end=-1&select=time,price,volume&_=1595411134728