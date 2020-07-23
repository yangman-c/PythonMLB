from sklearn.datasets import load_boston
import sys
import matplotlib.pyplot as plt

boston = load_boston()
print("data shape:{}".format(boston.data.shape))

import mglearn.datasets

x, y = mglearn.datasets.load_extended_boston()
print("x.shape:{}".format(x.shape))

mglearn.plots.plot_knn_classification(n_neighbors=3)
plt.show()

sys.exit()
