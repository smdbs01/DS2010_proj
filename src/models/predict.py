from collections import defaultdict
import pickle
import pandas as pd
import numpy as np
from os import path
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

from src.models import get_model
from src.models import save_model
from src import DATA_PATH
from src import MODEL_PATH

def predict(df: pd.DataFrame, model_name: str = "model.pkl") -> pd.DataFrame:
    model_path = path.join(MODEL_PATH, model_name)
    model = get_model(model_path)
    if model is None:
        return None
    
    X = df[['TIME OCC', 'LAT', 'LON']]
    
    print("Loading scalar...")
    scalar_path = path.join(MODEL_PATH, "scalar.pkl")
    with open(scalar_path, 'rb') as f:
        scalar = pickle.load(f)
        X = scalar.transform(X)
    
    print("Predicting...")
    return model.predict(X)

if __name__ == "__main__":
    test_path = path.join(DATA_PATH, "final", "crime_test.csv")
    test = pd.read_csv(test_path)
    
    y = test['Crm Cd Desc']
    
    res = predict(test)
    
    print(accuracy_score(y, res, normalize=True))
    
    # Plot
    true_count = defaultdict(int)
    false_count = defaultdict(int)
    
    true_pred_count = defaultdict(int)
    false_pred_count = defaultdict(int)
    
    for true, pred in zip(y, res):
        if true == pred:
            true_count[true] += 1
            true_pred_count[pred] += 1
        else:
            false_count[true] += 1
            false_pred_count[pred] += 1
    
    classes = list(true_count.keys())
    fig, ax = plt.subplots()
    x = np.arange(len(classes))
    width = 0.35
    
    ax.bar(x, [true_count[c] for c in classes], width, color="blue", label="True")
    ax.bar(x, [false_count[c] for c in classes], width, color="red", bottom=[true_count[c] for c in classes], label="False")
    ax.set_xlabel('Class')
    ax.set_ylabel('Number of Predictions')
    ax.set_title('Correct and Incorrect Predictions by Real Response Class')
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=45, ha='right')
    ax.legend()
    plt.show()
    
    # Prediction
    fig, ax = plt.subplots()
    
    ax.bar(x, [true_pred_count[c] for c in classes], width, color="blue", label="True")
    ax.bar(x, [false_pred_count[c] for c in classes], width, color="red", bottom=[true_pred_count[c] for c in classes], label="False")
    ax.set_xlabel('Class')
    ax.set_ylabel('Number of Predictions')
    ax.set_title('Correct and Incorrect Predictions by Predicted Class')
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=45, ha='right')
    ax.legend()
    plt.show()
    
    