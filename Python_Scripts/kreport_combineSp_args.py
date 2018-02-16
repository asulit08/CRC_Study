#!/usr/bin/env python

##script to get list of all TaxonIDs and Names from the Kreport files into 1 file and remove replicates

import sys
import glob
import os
import csv
import argparse
import os, os.path
from os.path import join
import pandas as pd


KreportCombine=argparse.ArgumentParser(description="List all unique Taxon ID's and their corresponding Taxon Names from Centrifuge Kreport files from indicated directory")

KreportCombine.add_argument("Kreport_Path", help = "directory where collection of Kreport files are to be found")

KreportCombine.add_argument("TaxonIDs", help = "output file where unique Taxon ID's and Names will be written to")

KreportCombine.add_argument("KreportList", help = "output file where comparison of reads per kreport per Taxon ID is written to ")

KreportCombine.add_argument("-s", "--species", action="store_true", help = "output will only give species data")

args=KreportCombine.parse_args()

kreport_path=glob.glob(join(args.Kreport_Path, '*/*.kreport')) ##specify all files ending in kreport
taxIDs=open(args.TaxonIDs, 'w')

def SortUniqueTaxIDs():

    Taxon=[]
    for report in kreport_path:
        file=open(report, 'r') 
        kreport_taxID=csv.reader(file, delimiter='\t') ##read kreport file

        for line in kreport_taxID:
            if args.species:
                if line[3]=='S': ##get only species 
                    Taxon.append(line[4] + '\t' + line[5].strip()) ##get taxon IDs and corresponding names,columns 5 and 6
            else:
                Taxon.append(line[4] + '\t' + line[5].strip()) ##get taxon IDs and corresponding names,columns 5 and 6 (ALL, regardless of species)

    SortTaxon = sorted(set(Taxon))
    
    for element in SortTaxon:
            row=element + '\n'
            taxIDs.write(row)

    taxIDs.close()

SortUniqueTaxIDs()

def KreportCombine():
    sorted_taxIDs=open(args.TaxonIDs, 'r') 
    sorted_taxIDs=open(args.TaxonIDs, 'r') ##open output of above function to read
    csv_sorttaxID=csv.reader(sorted_taxIDs, delimiter='\t') ## read output of above
    
    TaxID=[] ##list to put the TaxIDs into (first column of output above)
    TaxName=[] ##list to put corresponding TaxIDs into (2nd column of output above)
   
    for line in csv_sorttaxID: ## per line in output above
        TaxID.append(line[0]) ##add Taxon ID to list
        TaxName.append(line[1]) ##add Taxon Name to list
    
    ##to put Taxon Id and Taxon Names into Dictionary to make a dataframe in pandas; keys are column names/header, lists are data per column

    Dictionary={}
    Dictionary['TaxonID']=TaxID
    Dictionary['TaxonName']=TaxName

    Taxnames = pd.DataFrame(Dictionary) ## covnerts Dictionary to DataFrame named TaxNames

    ##combines read number output from kreports


    for report in kreport_path: ##each file ending in kreport
        ForReads=open(report, 'r') ##open each file ending in kreport
        csv_ForReads=csv.reader(ForReads, delimiter='\t')

        kreport_dict={} ##place values of interest in dictionary to map to Taxnames dataframe; keys are those that will map to (i.e. TaxonID)
        for line in csv_ForReads:
            if args.species:
                if line[3]=='S':
                    kreport_dict[line[4]]=line[2]
            else:
                kreport_dict[line[4]]=line[2]
               
        reportName=(report.split('/')[-1]).split('.')[0]
        Taxnames[reportName]=Taxnames.TaxonID.map(kreport_dict) ##map keys of dictionary to TaxonID column of data frame to get unique reads -- equivalent to vlookup or index-match of excel
        ForReads.close()
    
        TaxNamesFill=Taxnames.fillna(0)
    
        TaxNamesFill.to_csv(args.KreportList) ##write final data frame to file
    sorted_taxIDs.close()

KreportCombine()
