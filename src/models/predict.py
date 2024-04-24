import pickle
import pandas as pd
import numpy as np
from os import path

from src.models import get_model
from src.models import save_model
from src import DATA_PATH
from src import MODEL_PATH

def predict(df: pd.DataFrame) -> pd.DataFrame:
    model_path = path.join(MODEL_PATH, "model.pkl")
    model = get_model(model_path)
    if model is None:
        return None
    
    X = df[['TIME OCC', 'AREA', 'LAT', 'LON']]
    
    print("Loading scalar...")
    scalar_path = path.join(MODEL_PATH, "scalar.pkl")
    with open(scalar_path, 'rb') as f:
        scalar = pickle.load(f)
        X = scalar.transform(X)
    
    return model.predict(X)

if __name__ == "__main__":
    test_path = path.join(DATA_PATH, "final", "crime_test.csv")
    test = pd.read_csv(test_path)
    
    y = test['Crm Cd']
    
    res = predict(test)
    
    print(np.mean(res == y))
    
    