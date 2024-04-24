from os import path

DATA_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "data")
MODEL_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "models")

if __name__ == "__main__":
    print(DATA_PATH)
    print(MODEL_PATH)