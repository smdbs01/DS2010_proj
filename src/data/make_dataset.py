import requests
from os import path

DATA_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "..", "data")

# https://catalog.data.gov/dataset/crime-data-from-2020-to-present
URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"

def download_raw_data():
    p = path.join(DATA_PATH, "raw", "crime.csv")
    
    r = requests.get(URL, allow_redirects=True)
    
    if r.status_code != 200:
        print("Failed to download raw data. Status code:", r.status_code)
        return

    with open(p, 'wb') as f:
        f.write(r.content)

def main():
    if path.exists(path.join(DATA_PATH, "raw", "crime.csv")):
        print("Raw data already downloaded.")
        print("Type y to overwrite. Any other key to exit.")
        i = input()
        if i.upper() != "Y":
            return

    download_raw_data()

if __name__ == "__main__":
    main()
