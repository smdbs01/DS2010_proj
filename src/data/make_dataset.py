import requests
from os import path
import pandas as pd
import numpy as np

DATA_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "..", "data")

# https://catalog.data.gov/dataset/crime-data-from-2020-to-present
URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"

def download_raw_data(is_save: bool = False) -> pd.DataFrame:
    p = path.join(DATA_PATH, "raw", "crime.csv")
    
    if path.exists(p):
        print("Raw data already downloaded.")
        print("Type y to overwrite. Any other key to skip.")
        i = input()
        if i.upper() != "Y":
            return pd.read_csv(p)
    
    r = requests.get(URL, allow_redirects=True)
    
    if r.status_code != 200:
        print("Failed to download raw data. Status code:", r.status_code)
        return None
    
    if is_save:
        with open(p, 'wb') as f:
            f.write(r.content)
    
    print("Raw data downloaded.")
    df = pd.read_csv(p)
    return df

def clean_data(df: pd.DataFrame = None, is_save: bool = False) -> pd.DataFrame:
    cleaned_path = path.join(DATA_PATH, "processed", "crime.csv")
    
    if path.exists(cleaned_path):
        print("Processed data already exists.")
        print("Type y to overwrite. Any other key to skip.")
        i = input()
        if i.upper() != "Y":
            return pd.read_csv(cleaned_path)
    
    if df is None:
        p = path.join(DATA_PATH, "raw", "crime.csv")
        
        if not path.exists(p):
            print("Raw data not found. Downloading...")
            df = download_raw_data()
        else:
            print("Raw data already downloaded.")
            df = pd.read_csv(p)

    # drop duplicates
    df = df.drop_duplicates(subset=['DR_NO'])
    
    # remove rows missing LAT and LON
    df = df[(df[['LAT', 'LON']] != 0).all(axis=1)]
    
    if is_save:
        df.to_csv(cleaned_path, index=False)
    
    return df

def split_data(df: pd.DataFrame = None, seed: int = 42, train_size: float = 0.7, is_save: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    np.random.seed(seed)
    
    train_size = int(len(df) * train_size)
    
    shuffle = np.random.permutation(len(df))
    
    train = df.iloc[shuffle[:train_size]]
    test = df.iloc[shuffle[train_size:]]
    
    if is_save:
        train.to_csv(path.join(DATA_PATH, "final", "crime_train.csv"), index=False)
        test.to_csv(path.join(DATA_PATH, "final", "crime_test.csv"), index=False)
    
    return train, test

def main():
    df = download_raw_data(is_save=False)
    print("Raw data created.")
    
    df = clean_data(df, is_save=False)
    print("Processed data created.")

    train, test = split_data(df, is_save=True)
    print("Final train and test data saved.")

if __name__ == "__main__":
    main()
