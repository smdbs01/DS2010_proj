import requests
from os import path
import pandas as pd
import numpy as np

DATA_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "..", "data")

# https://catalog.data.gov/dataset/crime-data-from-2020-to-present
URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"

def download_raw_data() -> pd.DataFrame:
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

    with open(p, 'wb') as f:
        f.write(r.content)
    
    print("Raw data downloaded.")
    df = pd.read_csv(p)
    return df

def clean_data(df: pd.DataFrame):
    assert df is not None

    # drop duplicates
    df = df.drop_duplicates(subset=['DR_NO'])
    
    # remove rows missing LAT and LON
    df = df[(df[['LAT', 'LON']] != 0).all(axis=1)]
    
    return df

def split_data(df: pd.DataFrame, seed: int = 42, train_size: float = 0.7) -> tuple[pd.DataFrame, pd.DataFrame]:
    assert df is not None
    
    np.random.seed(seed)
    
    train_size = int(len(df) * train_size)
    
    shuffle = np.random.permutation(len(df))
    
    train = df.iloc[shuffle[:train_size]]
    test = df.iloc[shuffle[train_size:]]
    
    return train, test

def main():
    df = download_raw_data()
    df = clean_data(df)
    
    if not path.exists(path.join(DATA_PATH, "processed", "crime.csv")):
        df.to_csv(path.join(DATA_PATH, "processed", "crime.csv"), index=False)
    else:
        print("Processed data already exists. Type y to overwrite. Any other key to skip.")
        if input().upper() == "Y":
            df.to_csv(path.join(DATA_PATH, "processed", "crime.csv"), index=False)

    train, test = split_data(df)
    train.to_csv(path.join(DATA_PATH, "final", "crime_train.csv"), index=False)
    test.to_csv(path.join(DATA_PATH, "final", "crime_test.csv"), index=False)
    print("Processed data saved.")

if __name__ == "__main__":
    main()
