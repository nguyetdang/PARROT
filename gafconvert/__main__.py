# Import library
import argparse
from src.refbed_loader import refbed_loader
from src.vcgaf_loader import vcgaf_loader
from src.vcgaf2bed import vcgaf2bed
from src.vcgaf_panache_out import panache_out
from src.vcgaf_weighted_array import vcgaf_weighted_array

# Parser Argument
parser = argparse.ArgumentParser()
parser.add_argument("type", help="select input type", choices=['vcgaf'])
parser.add_argument("--refbed", help="path to reference bed file, required", required=True)
parser.add_argument("--gaf", help="path to gaf files, required", nargs='+', required=True)
parser.add_argument("--output", help="path to output, required", required=True)
parser.add_argument("--panache", help="output panache input format", action="store_true")
parser.add_argument("--biograph", help="output weighted array used in BioGraph.jl", action="store_true")
args = parser.parse_args()

# Convert input file into dataframe
refbed = refbed_loader(args.refbed)
vcgaf = vcgaf_loader(args.gaf)

# Prepare list of samples ID
samplename = []
for i in args.gaf:
    samplename.append(i.split('/')[-1].split('.')[0])

if args.type == 'vcgaf':
    if args.panache:
        result = panache_out(refbed, vcgaf, samplename)
        result.to_csv(args.output, sep='\t', index=False)
    elif args.biograph:
        result = vcgaf_weighted_array(refbed, vcgaf, samplename)
        result.to_csv(args.output, sep='\t', index=False, header=False)
    else:
        result = vcgaf2bed(refbed, vcgaf, samplename)
        result.to_csv(args.output, sep='\t', index=False)
