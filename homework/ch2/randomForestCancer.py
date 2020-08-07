from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

from homework.featureImport import plot_feature_importances_cancer

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=0)
forest = RandomForestClassifier(n_estimators=100, random_state=0)
forest.fit(X_train, y_train)

print("Accuracy on training set:{:.3f}".format(forest.score(X_train, y_train)))
print("Accuracy in test set:{:.3f}".format(forest.score(X_test, y_test)))

print("model.feature_importances_:{}", forest.feature_importances_)
print("cancer.data.shape[1]:{}", cancer.data.shape[1])
plot_feature_importances_cancer(forest.feature_importances_, cancer.data.shape[1], cancer.feature_names)