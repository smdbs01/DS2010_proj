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

def main():
    raw_path = path.join(DATA_PATH, "raw", "crime.csv")

    if not path.exists(raw_path):
        download_raw_data()
    
    df = pd.read_csv(raw_path)
    
    df = clean_data(df)
    
    print(df)
    
    cleaned_path = path.join(DATA_PATH, "processed", "crime.csv")

    if path.exists(cleaned_path):
        print("Cleaned data already exists. Type y to overwrite. Any other key to exit.")
        i = input()
        if i.upper() != "Y":
            return
    df.to_csv(cleaned_path, index=False)

if __name__ == "__main__":
    main()