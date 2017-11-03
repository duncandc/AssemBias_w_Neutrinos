"""
read the header in the ROCKSTAR halo catalogue ascii files to make processing easier
"""

#load packages
from __future__ import print_function, division
import re
import sys

__all__ = ['read_header']

def main():
    """
    print out the column names and number
    """
    
    #set the ascii file to process
    if len(sys.argv)>1:
        fname = sys.argv[1]
    else:
        filepath = './'
        filename = 'out_66_massless.list'
        fname = filepath + filename
    
    col_names, d = read_header(fname)
    for i,name in enumerate(col_names):
        print(i, name)

    for key in d.keys():
        print(key, d[key])


def read_header(fname):
    """
    read the first lines of a ROCKSTAR hlist files and return a list of column names
    """
    
    d = {} #dictionary to store sim info
    
    units = ['Mpc/h','Msun/h'] #strip these of keys if you find them

    with open(fname, 'r') as f:
        first_line = f.readline()
        cols_info = first_line.split(' ')
        col_names = []
        for col_info in cols_info:
            col_name = col_info.split('(')[0].strip('#')
            col_names.append(col_name)
        
        comment=True
        while comment==True:
            next_line = f.readline()
            if next_line[0]=='#': 
                line = next_line[1:]
                comment=True
                if ';' in line:
                    for bit in line.split(';'):
                        if '=' in bit:
                            key = bit.split('=')[0].strip()
                            value = bit.split('=')[1].strip('\n')
                        if ':' in bit:
                            key = bit.split(':')[0].strip()
                            value = bit.split(':')[1].strip('\n')
                        for unit in units:
                            value = value.strip(unit)
                        d[key]=value
                elif '=' in line:
                    key = line.split('=')[0].strip()
                    value = line.split('=')[1].strip('\n')
                    for unit in units:
                        value = value.strip(unit)
                        d[key]=value
                elif ':' in line:
                    key = line.split(':')[0].strip()
                    value = line.split(':')[1].strip('\n')
                    for unit in units:
                        value = value.strip(unit)
                        d[key]=value
            else: comment=False

    return col_names, d

if __name__ == '__main__':
    main()