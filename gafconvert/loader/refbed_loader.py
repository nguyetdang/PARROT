from gafconvert.builtin import pd

def refbed_loader(refbedpath):
    refbed = pd.read_table(refbedpath, header = None)
    refbed.rename(columns = {0: "SegName", 1: "Start", 2: "End", 4: "SegID"})
    return refbed
