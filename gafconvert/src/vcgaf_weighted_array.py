import pandas as pd
from collections import Counter


def mappath_counter(mappath):
    return dict(Counter(mappath.replace(">", " ").replace("<", " ").split(" ")[1:]))


def total_mappath_counter(mappathlist):
    total_counter = {}
    for mappath in mappathlist:
        total_counter = dict(Counter(total_counter) + Counter(mappath))
    for key, value in total_counter.items():
        total_counter[key] = 1
    return total_counter


def vcgaf_weighted_array(refbed, vcgaf, sampleID):

    # prepare counter dictionary from refbed
    refcounter = {}
    for key in refbed.SegID:
        refcounter[key] = 1

    # prepare counter dictionary for each sample gaf file and put the results in a list
    gafcount = []
    for singlegaf in vcgaf:
        singlegaf = pd.DataFrame(singlegaf)
        gafcount.append(total_mappath_counter(singlegaf.apply(lambda row: mappath_counter(row.MapPath), axis=1)))
    gafcount.append(refcounter)
    result = total_mappath_counter(gafcount)
    result_out = []
    for key, value in result.items():
        result_out.append((key, value))
    result_out = pd.DataFrame(result_out)
    return result_out
