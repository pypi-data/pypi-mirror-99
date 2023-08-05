#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Stephan Fuchs (Robert Koch Institute, MF-1, fuchss@rki.de)

VERSION = "0.0.9"
import os
import argparse
import re
import sys


def main():
    parser = argparse.ArgumentParser(prog="create_bedpe.py", description="create a bedpe file used for bamclipper based on two BED files containing the amplicon and the insert coordinates, respectively.", )
    parser.add_argument('files', metavar="FILE", help="fastq files", type=str, nargs="+")
    parser.add_argument('--regex', metavar="STR", help="regex to extract sample name from filename including absolute path (sample name must be stored in group 1 of regex)", type=str, default=None)
    parser.add_argument('--mf2', help="use regex for MF2 sample naming scheme", action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    args = parser.parse_args()
    
    if args.mf2 and args.regex:
        sys.exit("error: --regex and --mf2 are mutuallz exlcusive options.")
    elif args.mf2:
        regex = re.compile(r"./[^_]*_[^_]*_([0-9a-zA-Z-_]+)_S[0-9]{1,2}_.*")
    elif args.regex:
        regex = re.compile(args.regex) 
    else:
        regex = None

    for i in range(0,len(args.files), 2):    
        read1 = os.path.abspath(args.files[i])
        read2 = os.path.abspath(args.files[i+1])
        if not regex:
            alt = args.files[i]
        else:
            alt = regex.search(read1)
            if not alt:
                sys.exit("error not regex match for file pair " + read1 + ", " + read2)
            alt = alt.group(1)
            alt2 = regex.search(read2).group(1)
            if alt != alt2:
                sys.exit("error: given regex leads to different sample names for file pair" + read1 + "(" + alt + "), " + read2 + "(" + alt2 + ")")
        
        print('"'+alt+'":')
        print('  alt_id: Sample_' + str(int(i/2)+1))
        print('  read1: "' + read1 + '"')
        print('  read2: "' + read2 + '"')

if __name__ == "__main__":
        main()
