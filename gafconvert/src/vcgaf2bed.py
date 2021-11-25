import pandas as pd
from collections import Counter


def mappath_counter(mappath):
    return dict(Counter(mappath.replace(">", " >").replace("<", " <").split(" ")[1:]))


def total_mappath_counter(mappathlist):
    total_counter = {}
    for mappath in mappathlist:
        total_counter = dict(Counter(total_counter) + Counter(mappath))
    return total_counter


def vcgaf2bed(refbed, vcgaf, sampleID):

    # prepare counter dictionary from refbed
    refbed1 = refbed.apply(lambda x: '>' + x if x.name == 'SegID' else x)
    refbed2 = refbed.apply(lambda x: '<' + x if x.name == 'SegID' else x)
    newrefbed = pd.concat([refbed1, refbed2], ignore_index=True, sort=False)
    refcounter = {}
    for key in newrefbed.SegID:
        refcounter[key] = 1

    # prepare counter dictionary for each sample gaf file and put the results in a list
    gafcount = []
    for singlegaf in vcgaf:
        singlegaf = pd.DataFrame(singlegaf)
        gafcount.append(total_mappath_counter(singlegaf.apply(lambda row: mappath_counter(row.MapPath), axis=1)))

    # prepare full counter with all the SegID
    gafcountfull = []
    for eachcount in gafcount:
        newelement = total_mappath_counter([refcounter, eachcount])
        for key, value in newelement.items():
            newelement[key] = value - 1
        gafcountfull.append(newelement)

    # prepare output bed file with sampleID
    outputdict = newrefbed.copy()
    samplecount = dict(zip(sampleID, gafcountfull))
    for key, value in samplecount.items():
        new_d = pd.Series(value)
        outputdict[key] = outputdict['SegID'].map(new_d)

    return outputdict
