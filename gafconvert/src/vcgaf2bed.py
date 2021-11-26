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
    print("Finish prepared reference file")
    # prepare counter dictionary for each sample gaf file and put the results in a list
    gafcount = []
    i = 0
    for singlegaf in vcgaf:
        print("Start processing individual " + str(i) + " - " + str(sampleID[i]))
        singlegaf = pd.DataFrame(singlegaf)
        singlegafcount = total_mappath_counter(singlegaf.apply(lambda row: mappath_counter(row.MapPath), axis=1))
        print("Finish individual counting process" + str(i))
        singlegafcountfull = total_mappath_counter([refcounter, singlegafcount])
        for key, value in singlegafcountfull.items():
            singlegafcountfull[key] = value - 1
        gafcount.append(singlegafcountfull)
        i = i + 1
    # prepare dictionary for output
    outputdict = newrefbed.copy()
    samplecount = dict(zip(sampleID, gafcount))
    for key, value in samplecount.items():
        new_d = pd.Series(value)
        outputdict[key] = outputdict['SegID'].map(new_d)
    return outputdict
