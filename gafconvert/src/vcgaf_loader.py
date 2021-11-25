import pandas as pd


def vcgaf_loader(vcgafpath):
    vcgaf = []
    for path in vcgafpath:
        vcgafitem = pd.read_table(path, header=None)
        vcgafitem = vcgafitem.rename(columns={0: "QSegName", 1: "QSegLen", 2: "QSegStart", 3: "QSegEnd",
                                              4: "QSegDrt", 5: "MapPath", 6: "PathLen", 7: "PathStart",
                                              8: "PathEnd", 9: "NoResMatched", 10: "AlnBlockLen",
                                              11: "MapQual"})
        vcgaf.append(vcgafitem)
    return vcgaf
