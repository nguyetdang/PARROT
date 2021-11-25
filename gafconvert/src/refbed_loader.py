import pandas as pd


def refbed_loader(refbedpath):
    refbed = pd.read_table(refbedpath, header=None)
    refbed = refbed.rename(columns={0: "SegName", 1: "Start", 2: "End", 3: "SegID"})
    return refbed
