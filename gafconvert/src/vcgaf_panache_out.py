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
    i = 0
    for singlegaf in vcgaf:
        print("Start processing individual " + str(i) + " - " + str(sampleID[i]))
        singlegaf = pd.DataFrame(singlegaf)
        singlegafcount = panache_total_mappath_counter(singlegaf.apply(lambda row: panache_mappath_counter(row.MapPath),
                                                                       axis=1))
        print("Finish individual counting process" + str(i))
        singlegafcountfull = panache_total_mappath_counter([refcounter, singlegafcount])
        for key, value in singlegafcountfull.items():
            singlegafcountfull[key] = value - 1
        gafcount.append(singlegafcountfull)
        i = i + 1

    # prepare output bed file with sampleID
    outputdict = refbed.copy()
    outputdict["Sequence_IUPAC_Plus"] = "."
    outputdict["SimilarBlocks"] = "."
    outputdict["Function"] = "."
    outputdict = outputdict.rename(columns={"SegName": "#Chromosome", "Start": "FeatureStart",
                                            "End": "FeatureStop"})
    samplecount = dict(zip(sampleID, gafcount))
    for key, value in samplecount.items():
        new_d = pd.Series(value)
        outputdict[key] = outputdict['SegID'].map(new_d)
    outputdict = outputdict.drop('SegID', axis=1)
    return outputdict
