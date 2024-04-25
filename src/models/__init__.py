import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from os.path import exists

def get_model(path: str) -> RandomForestClassifier:
    if not exists(path):
        print("Model not found. Is there a pretrained model?")
        return None
    
    print("Model found. Loading model...")
    return pd.read_pickle(path)

def save_model(model: RandomForestClassifier, path: str) -> None:
    print("Saving model...")
    pd.to_pickle(model, path)
    print("Model saved.")