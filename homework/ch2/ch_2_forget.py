import mglearn.datasets
import matplotlib.pyplot as plt
import mglearn.plots
import sys
from sklearn.model_selection import  train_test_split

#生成数据集
X,y = mglearn.datasets.make_forge()
#数据集绘图
mglearn.discrete_scatter(X[:,0], X[:,1], y)
plt.legend(["Class 0", "Class 1"], loc=4)
plt.xlabel("First feature")
plt.ylabel("Second feature")
print("X.shape:{}".format(X.shape))


mglearn.plots.plot_knn_classification(n_neighbors=3)
# plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)

print("Test set predications:{}".format(clf.predict(X_test)))
print("Test set accuracy:{:.2f}".format(clf.score(X_test, y_test)))

fig, axes = plt.subplots(1,3,figsize=(10, 3))

for n_neighbors, ax in zip([1,3,9], axes):
    clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
    mglearn.plots.plot_2d_classification(clf, X, fill=True, eps=0.5, ax=ax, alpha=0.4)
    mglearn.discrete_scatter(X[:,0], X[:, 1], y, ax=ax)
    ax.set_title("{} neighbor(s)".format(n_neighbors))
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")
axes[0].legend(loc=3)
# plt.show()

sys.exit()