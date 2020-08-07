from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import mglearn.plots
cancer = load_breast_cancer()
X_Train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target, random_state=42)
# tree = DecisionTreeClassifier(random_state=0)
tree = DecisionTreeClassifier(max_depth=4, random_state=0)
tree.fit(X_Train, y_train)
print("Accuracy on training set:{:.3f}".format(tree.score(X_Train, y_train)))
print("Accuracy on test set:{:.3f}".format(tree.score(X_test, y_test)))

from sklearn.tree import export_graphviz
export_graphviz(tree, out_file="tree.dot", class_names=["malignant", "benign"], feature_names=cancer.feature_names, impurity=False, filled=True)

import graphviz
with open("tree.dot") as f:
    dot_graph = f.read()
src = graphviz.Source(dot_graph).copy()

print("Feature importances:\n{}".format(tree.feature_importances_))

import homework.featureImport as fi
fi.plot_feature_importances_cancer(tree.feature_importances_, cancer.data.shape[1], cancer.feature_names)
mglearn.plots.plot_tree_not_monotone()
display(tree)