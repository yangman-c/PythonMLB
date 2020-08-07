import mglearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sys

X, y = mglearn.datasets.load_extended_boston()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
lr = LinearRegression().fit(X_train, y_train)

print("Training set score:{:.2f}".format(lr.score(X_train, y_train)))
print("Test set score:{:.2f}".format(lr.score(X_test, y_test)))

from sklearn.linear_model import Ridge
alphas = range(1, 11)
for alpha in alphas:
    ridge = Ridge(alpha=alpha).fit(X_train, y_train)
    print("alpha:{} Trainning set score:{:.2f} Test set score:{:.2f}".format(alpha, ridge.score(X_train, y_train), ridge.score(X_test, y_test)))
    plt.plot(ridge.coef_, 's', label="Ridge alpha={}".format(alpha))

sys.exit()
