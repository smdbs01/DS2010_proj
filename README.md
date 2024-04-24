## Description

This project aims to build a machine learning model that predicts the type of crime committed in a given area during a given time.

## Run

1. Make sure you have a proper Python version. The author has Python 3.11.7, so any other version may not work as expected.

1. Install the required libraries using `pip install -r requirements.txt`. This might fail if you have a different version of Python.

1. Get the dataset using `python -m src.data.make_dataset`. This will create `data/final/crime_train.csv` and `data/final/crime_test.csv`. If you would like to access the raw data, you can download it directly from [https://catalog.data.gov/dataset/crime-data-from-2020-to-present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present) or change the `is_save` parameter in `src/data/make_dataset.py` to `True`.

1. Train the model using `python -m src.models.train`.

1. Test the model on the test dataset using `python -m src.models.test`.

## Data Source

[https://catalog.data.gov/dataset/crime-data-from-2020-to-present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)

The dataset used by this project was downloaded on 4-20-2024.
