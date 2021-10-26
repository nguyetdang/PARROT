### Import library
import argparse
import refbed_loader, vcgaf_loader

### Parser Argument
parser = argparse.ArgumentParser()
parser.add_argument("type", help="select input type", choices=['vcgaf'])
parser.add_argument("--refbed", help="path to reference bed file, required", required=True)
parser.add_argument("--gaf", help="path to gaf file, required", required=True)
parser.add_argument("--output", help="path to output, required", required=True)
parser.add_argument("--panache", help="output panache input format", action="store_true")
parser.add_argument("--biograph", help="output weighted array used in BioGraph.jl", action="store_true")
args = parser.parse_args()

### Convert vcgaf file
refbed = refbed_loader(args.refbed)
vcgaf = vcgaf_loader(args.gaf)

