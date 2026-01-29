import pandas as pd

# Simple CSV extraction utility
def extract_csv(path, chunk_size):
    """
    Reads a CSV file in chunks to avoid loading the entire file into memory.

    Args:
        path (str): Filesystem path to the CSV file.
        chunk_size (int): Number of rows per chunk to read.

    Returns:
        TextFileReader: An iterator over DataFrame chunks (pandas TextFileReader).
    """
    # Use pandas read_csv with the chunksize parameter to return an iterator
    return pd.read_csv(path, chunksize=chunk_size)
