import pandas as pd
import numpy as np
from os import path

from src import DATA_PATH

def split_data(df: pd.DataFrame, seed: int = 42, train_size: float = 0.7) -> tuple[pd.DataFrame, pd.DataFrame]:
    assert df is not None
    
    np.random.seed(seed)
    
    train_size = int(len(df) * train_size)
    
    shuffle = np.random.permutation(len(df))
    
    train = df.iloc[shuffle[:train_size]]
    test = df.iloc[shuffle[train_size:]]
    
    return train, test

def main():
    cleaned_path = path.join(DATA_PATH, "processed", "crime.csv")
    
    if not path.exists(cleaned_path):
        print("Cleaned data does not exist. Run `python -m src.data.make_dataset` first.")
        return
    
    df = pd.read_csv(cleaned_path)
    
    train, test = split_data(df)
    
    train_path = path.join(DATA_PATH, "final", "crime_train.csv")
    test_path = path.join(DATA_PATH, "final", "crime_test.csv")
    
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)

if __name__ == "__main__":
    main()