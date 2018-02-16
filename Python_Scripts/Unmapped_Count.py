#!/usr/bin/env python

import os, os.path
import re
import glob
import sys
import argparse
from os.path import splitext
import pandas as pd

UnmappedReadCount=argparse.ArgumentParser(description="output readcounts of sample inputs to centrifuge")

UnmappedReadCount.add_argument("dir1", help="one directory containing the input files")
UnmappedReadCount.add_argument("dir2", help="2nd directory containing the input files")
UnmappedReadCount.add_argument("combined_kreport", help="Initial Combined Kreport from Centrifuge outputs")
UnmappedReadCount.add_argument("outfile", help="output containing tables of Taxon IDs and Read Counts")

args=UnmappedReadCount.parse_args()

path1=glob.glob(args.dir1 + "*/*.mate1*") ##all files contain .mate1 whether single or paired

FileName=re.compile('^(\d+)-(\d+)-(\d+)-(\d+)')
Base=re.compile('(\d+)-(\d+)-(\d+)-(\d+)$')
Read_Counts_Dict={}

for file1 in path1:
    Filename1=(file1.split('/')[-1])
    
    if re.search(FileName,Filename1):
        FQ1=open(file1, 'r')
        Reads1=0
        for line1 in FQ1:
             if line1.startswith('@'): 
                 Reads1+=1
        
        if file1.endswith('.fq'):
            Name1=(file1.split('/')[-1]).split('.')[0] 
        else:
            Name1=(file1.split('/')[-1]).split('_')[0]
        
        Basename1=Base.match(Name1)
        if Basename1:
            Name1=Name1
        else:
            Name1=(Name1.split('_'))[0]
        
        if Name1 not in Read_Counts_Dict:
            Read_Counts_Dict[Name1]=[Reads1]
        else:
            Read_Counts_Dict[Name1].append(Reads1)


path2=glob.glob(args.dir2 + "*/*.mate1*")
for file2 in path2:
    Filename2=(file2.split('/')[-1])
    
    if re.search(FileName,Filename2):
        FQ2=open(file2, 'r')
        Reads2=0
        for line2 in FQ2:
             if line2.startswith('@'): 
                 Reads2+=1
        
        if file2.endswith('.fq'):
            Name2=(file2.split('/')[-1]).split('.')[0] 
        else:
            Name2=(file2.split('/')[-1]).split('_')[0]
        
        Basename2=Base.match(Name2)
        if Basename2:
            Name2=Name2
        else:
            Name2=(Name2.split('_'))[0]
        
        if Name2 not in Read_Counts_Dict:
            Read_Counts_Dict[Name2]=[Reads2]
        else:
            Read_Counts_Dict[Name2].append(Reads2)
    
for key in Read_Counts_Dict:
    Read_Counts_Dict[key]=[sum(Read_Counts_Dict[key])]

Read_Counts_Dict['TaxonName']=['Read_Count']

ReadCounts_df=pd.DataFrame(Read_Counts_Dict)
print(ReadCounts_df)

Kreport=pd.read_csv(args.combined_kreport)

ConcatenatedFinal = pd.concat([ReadCounts_df,Kreport], axis=0)

ConcatenatedFinal.to_csv(args.outfile)