from gafconvert.src.refbed_loader import refbed_loader
from gafconvert.src.vcgaf_loader import vcgaf_loader
from gafconvert.src.vcgaf2bed import vcgaf2bed


refbedpath = "/Users/nguyetdang/bioinfo/platGB2_r426.bed"
samplepath = ("/Users/nguyetdang/bioinfo/invimap_vc_platGB2/test1.paf",
              "/Users/nguyetdang/bioinfo/invimap_vc_platGB2/test2.paf")

refbed = refbed_loader(refbedpath)
samplegaf = vcgaf_loader(samplepath)

sampleID = []
for i in samplepath:
    sampleID.append(i.split('/')[-1].split('.')[0])

result = vcgaf2bed(refbed, samplegaf, sampleID)
result.to_csv('output.txt', sep='\t', index=False)
