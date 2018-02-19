#!/usr/bin/env python

import sys
import glob
import os
import csv
import argparse
import os, os.path
from os.path import join
import pandas as pd

Kreport_Counts=argparse.ArgumentParser(description="List unclassified and root read counts for each sample")
Kreport_Counts.add_argument("Kreport_Path", help = "directory where collection of Kreport files are to be found")
Kreport_Counts.add_argument("output", help = "output containing counts of unclassified and root counts")

args=Kreport_Counts.parse_args()

kreport_path=glob.glob(join(args.Kreport_Path, '*/*.kreport'))
counts= open(args.output, 'w')

header = 'sample' + '\t' + "unclassified" + '\t' + "root" + '\n'
#print(header)
counts.write(header)


for report in kreport_path:
    file=open(report, 'r')
    kreport=csv.reader(file, delimiter='\t')
    
    unclassified=""
    root= ""
    for line in kreport:
        if line[4] == "0":
            unclassified += line[1]
        elif line[4] == "1":
            root += line[1]
        else:
            continue
     
    name=(report.split('/')[-1]).split('.')[0]
    row= name + '\t' + unclassified + '\t' + root + '\n'
    counts.write(row)
    #print(row)
  

            