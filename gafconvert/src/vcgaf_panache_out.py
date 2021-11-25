import pandas as pd
from collections import Counter


def panache_mappath_counter(mappath):
    return dict(Counter(mappath.replace(">", " ").replace("<", " ").split(" ")[1:]))


def panache_total_mappath_counter(mappathlist):
    total_counter = {}
    for mappath in mappathlist:
        total_counter = dict(Counter(total_counter) + Counter(mappath))
    return total_counter


def panache_out(refbed, vcgaf, sampleID):

    # prepare counter dictionary from refbed
    refcounter = {}
    for key in refbed.SegID:
        refcounter[key] = 1

    # prepare counter dictionary for each sample gaf file and put the results in a list
    gafcount = []
    for singlegaf in vcgaf:
        singlegaf = pd.DataFrame(singlegaf)
        gafcount.append(panache_total_mappath_counter(singlegaf.apply(lambda row: panache_mappath_counter(row.MapPath),
                                                                      axis=1)))

    # prepare full counter with all the SegID
    gafcountfull = []
    for eachcount in gafcount:
        newelement = panache_total_mappath_counter([refcounter, eachcount])
        for key, value in newelement.items():
            newelement[key] = value - 1
        gafcountfull.append(newelement)

    # prepare output bed file with sampleID
    outputdict = refbed.copy()
    outputdict["Sequence_IUPAC_Plus"] = "."
    outputdict["SimilarBlocks"] = "."
    outputdict["Function"] = "."
    outputdict = outputdict.rename(columns={"SegName": "#Chromosome", "Start": "FeatureStart",
                                            "End": "FeatureStop"})
    samplecount = dict(zip(sampleID, gafcountfull))
    for key, value in samplecount.items():
        new_d = pd.Series(value)
        outputdict[key] = outputdict['SegID'].map(new_d)
    outputdict = outputdict.drop('SegID', axis=1)
    return outputdict
