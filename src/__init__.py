from os import path

DATA_PATH = path.join((path.abspath(path.dirname(__file__))), "..", "data")

if __name__ == "__main__":
    print(DATA_PATH)