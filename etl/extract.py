import pandas as pd

def extract_csv(path, chunk_size):
    return pd.read_csv(path, chunksize=chunk_size)
