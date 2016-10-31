import csv
import os
import sys

import numpy as np
from pandas import DataFrame


class XTREError(Exception):
    pass


def say(text):
    sys.stdout.write(str(text))


def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df


def read_chunked_csv(f):
    """ chuck csv at ' --- ' and generate a dataframe
    """
    holder = []
    with open(f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, row in enumerate(csvreader):
            if i == 0:
                header = row
            elif not any(['-' in r for r in row]):
                holder.append([float(r) for r in row])
            else:
                yield DataFrame(holder, columns=header)
                holder = []  # Flush out holder


def csv2df(directory):
    files = [df for df in read_chunked_csv(directory)]
    return files


def explore(directory, method='NSGAIII'):
    for (dirpath, dirnames, filenames) in os.walk(directory):
        pass

    for file in filenames:
        if method.lower() in file.lower():
            return csv2df(os.path.join(dirpath, file))
