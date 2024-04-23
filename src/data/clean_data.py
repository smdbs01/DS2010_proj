import pandas as pd
from os import path

from src import DATA_PATH
from src.data.make_dataset import download_raw_data

def clean_data(df: pd.DataFrame):
    assert df is not None

    # drop duplicates
    df = df.drop_duplicates(subset=['DR_NO'])
    
    # remove rows missing LAT and LON
    df = df[(df[['LAT', 'LON']] != 0).all(axis=1)]
    
    return df

if __name__ == "__main__":
    raw_path = path.join(DATA_PATH, "raw", "crime.csv")

    if not path.exists(raw_path):
        download_raw_data()
    
    df = pd.read_csv(raw_path)
    
    print(clean_data(df))