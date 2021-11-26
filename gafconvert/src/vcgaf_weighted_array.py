import pandas as pd
from collections import Counter


def mappath_counter(mappath):
    return dict(Counter(mappath.replace(">", " ").replace("<", " ").split(" ")[1:]))


def total_mappath_counter(mappathlist):
    total_counter = {}
    for mappath in mappathlist:
        total_counter = dict(Counter(total_counter) + Counter(mappath))
    return total_counter


def vcgaf_weighted_array(refbed, vcgaf, sampleID):

    # prepare counter dictionary from refbed
    refcounter = {}
    for key in refbed.SegID:
        refcounter[key] = 1

    # prepare counter dictionary for each sample gaf file and put the results in a list
    #gafcount = []
    #for singlegaf in vcgaf:
    #    singlegaf = pd.DataFrame(singlegaf)
    #    gafcount.append(total_mappath_counter(singlegaf.apply(lambda row: mappath_counter(row.MapPath), axis=1)))
    #gafcount.append(refcounter)

    ####
    gafcount = []
    i = 0
    for singlegaf in vcgaf:
        print("Start processing individual " + str(i) + " - " + str(sampleID[i]))
        singlegaf = pd.DataFrame(singlegaf)
        singlegafcount = total_mappath_counter(singlegaf.apply(lambda row: mappath_counter(row.MapPath), axis=1))

        # Fix appearance = 1
        for key, value in singlegafcount.items():
            singlegafcount[key] = 1
        print("Finish individual counting process" + str(i))
        gafcount.append(singlegafcount)
        i = i + 1
    gafcount.append(refcounter)
    result = total_mappath_counter(gafcount)
    result_out = []
    for key, value in result.items():
        result_out.append((key, value - 1))
    result_out = pd.DataFrame(result_out)
    return result_out
