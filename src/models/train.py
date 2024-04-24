import numpy as np
import pandas as pd
from os import path
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

from src import DATA_PATH
from src import MODEL_PATH
from src.models import get_model
from src.models import save_model

def train_model(df: pd.DataFrame, *args, **kwargs) -> None:
    model_path = path.join(MODEL_PATH, "model.pkl")
    model = get_model(model_path)
    if model is None:
        print("Creating new model.")
        model = RandomForestClassifier(*args, **kwargs)
    
    # Time, Area, Latitude, Longitude of the reported crime
    X = df[['TIME OCC', 'AREA', 'LAT', 'LON']]
    # The code of the crime (type of crime)
    y = df['Crm Cd']
    
    scalar = StandardScaler()
    X = scalar.fit_transform(X)
    
    print("Training model...")
    model.fit(X, y)
    print("Training ended.")
    
    scalar_path = path.join(MODEL_PATH, "scalar.pkl")
    with open(scalar_path, 'wb') as f:
        pickle.dump(scalar, f)
    
    save_model(model, model_path)
    
if __name__ == "__main__":
    train_path = path.join(DATA_PATH, "final", "crime_train.csv")
    
    train = pd.read_csv(train_path)
    
    train_model(train, n_estimators=100, max_depth=10)

    
    