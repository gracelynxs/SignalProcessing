from ont_fast5_api.fast5_interface import get_fast5_file
import csv
import numpy as np
import os

#Testing Function
def print_all_raw_data():
    fast5_filepath = 'src\\batch22.fast5' # This can be a single- or multi-read file
    with get_fast5_file(fast5_filepath, mode="r") as f5:
        for read in f5.get_reads():
            raw_data = read.get_raw_data()
            raw_data = raw_data.flatten()
            with open("newfile.csv", 'w', newline = '') as outfile:
                csv_writer = csv.writer(outfile, delimiter = ',')
                csv_writer.writerow(raw_data)
            #raw data is a numpy array...
            print(read.read_id, raw_data)
    return 0

#Need to have a bundling function

def read_2(file1, file2):
    pass

#REQUIRES THAT THE FILE INPUT IS THE SAME AS THE PATH!
def read_file(file):
    path = str(file)
    with get_fast5_file(path, mode="r") as f5:
        for read in f5.get_reads():
            raw_data = read.get_raw_data()
            raw_data = raw_data.flatten()
            with open( path+'.csv', 'w', newline = '') as outfile:
                csv_writer = csv.writer(outfile, delimiter = ',')
                csv_writer.writerow(raw_data)
            print(read.read_id, raw_data)

#Built for reading a custom, bound file type. 
def read_custom(file):
    pass