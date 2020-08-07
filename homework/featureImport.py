import matplotlib.pyplot as plt
import numpy as np

def plot_feature_importances_cancer(featureImportance, numFeature, feature_names):
    plt.barh(range(numFeature), featureImportance, align='center')
    plt.yticks(np.arange(numFeature), feature_names)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.show()