import requests
import os.path as path

# https://catalog.data.gov/dataset/crime-data-from-2020-to-present
URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"

def download_raw_data():
    p = path.join((path.abspath(path.dirname(__file__))), "..", "..", "data", "raw", "crime.csv")
    
    r = requests.get(URL, allow_redirects=True)

    with open(p, 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    download_raw_data()
    