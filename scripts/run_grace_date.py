#!/usr/bin/env python
u"""
run_grace_date.py
Written by Tyler Sutterley (10/2021)

Wrapper program for running GRACE date and months programs

Processing Centers: [CSR, GFZ, JPL]
Data Releases CSR, GFZ, JPL: RL06
Data Products: [GAA, GAB, GAC, GAD, GSM]
    CSR: (GAC, GAD, GSM) only

CALLING SEQUENCE:
    run_grace_date(base_dir, PROC, DREL, VERBOSE=False)

INPUTS:
    base_dir: working GRACE/GRACE-FO data directory
    PROC: GRACE/GRACE-FO data processing center
        CSR: University of Texas Center for Space Research
        GFZ: German Research Centre for Geosciences (GeoForschungsZentrum)
        JPL: Jet Propulsion Laboratory
    DREL: GRACE/GRACE-FO data release to run

OPTIONS:
    VERBOSE: Track program progress
    MODE: permissions mode of output date files

COMMAND LINE OPTIONS:
    -D X, --directory X: GRACE/GRACE-FO working data directory
    -C X, --center X: GRACE/GRACE-FO Processing Center (CSR,GFZ,JPL)
    -R X, --release X: GRACE/GRACE-FO data releases (RL04,RL05,RL06)
    -V, --verbose: Track program progress
    -M X, --mode X: Permissions mode of output date files

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
    dateutil: powerful extensions to datetime
        https://dateutil.readthedocs.io/en/stable/
    future: Compatibility layer between Python 2 and Python 3
        https://python-future.org/

PROGRAM DEPENDENCIES:
    grace_date.py: computes the dates of the GRACE/GRACE-FO datasets
    time.py: utilities for calculating time operations
    grace_months_index.py: creates a single file showing the GRACE dates

UPDATE HISTORY:
    Updated 10/2021: using python logging for handling verbose output
    Updated 09/2021: using verbose option to track program progress
    Updated 05/2021: define int/float precision to prevent deprecation warning
    Updated 10/2020: use argparse to set command line parameters
    Updated 05/2020: updated for public release
    Updated 10/2019: changing Y/N flags to True/False
    Updated 08/2018: added GFZ RL06 parameters for LMAX 60
        using full release string (RL05 instead of 5)
    Updated 06/2018: using python3 compatible octal and input. RL06 updates.
        if running as program: will use inputs from getopt
    Updated 01/2017: added MODE to set file and directory permissions
    Updated 05/2016: using __future__ print function
    Updated 11/2015: switched to dictionaries only. cleaned up obsolete portions
    Updated 12/2014: added main definition for running from the command line
    Updated 02/2014: minor update to if statements
    Written 07/2012
"""
from __future__ import print_function

import sys
import os
import logging
import argparse
from gravity_toolkit.grace_date import grace_date
from gravity_toolkit.grace_months_index import grace_months_index

def run_grace_date(base_dir, PROC, DREL, VERBOSE=False, MODE=0o775):
    #-- create logger
    loglevel = logging.INFO if VERBOSE else logging.CRITICAL
    logging.basicConfig(level=loglevel)

    #-- allocate python dictionaries for each processing center
    DSET = {}
    VALID = {}
    #-- CSR RL04/5/6 at LMAX 60
    DSET['CSR'] = {'RL04':['GAC', 'GAD', 'GSM'], 'RL05':['GAC', 'GAD', 'GSM'],
        'RL06':['GAC', 'GAD', 'GSM']}
    VALID['CSR'] = ['RL04','RL05','RL06']
    #-- GFZ RL04/5 at LMAX 90
    #-- GFZ RL06 at LMAX 60
    DSET['GFZ'] = {'RL04':['GAA', 'GAB', 'GAC', 'GAD', 'GSM'],
        'RL05':['GAA', 'GAB', 'GAC', 'GAD', 'GSM'],
        'RL06':['GAA', 'GAB', 'GAC', 'GAD', 'GSM']}
    VALID['GFZ'] = ['RL04','RL05','RL06']
    #-- JPL RL04/5/6 at LMAX 60
    DSET['JPL'] = {'RL04':['GAA', 'GAB', 'GAC', 'GAD', 'GSM'],
        'RL05':['GAA', 'GAB', 'GAC', 'GAD', 'GSM'],
        'RL06':['GAA', 'GAB', 'GAC', 'GAD', 'GSM']}
    VALID['JPL'] = ['RL04','RL05','RL06']

    #-- for each processing center
    for p in PROC:
        #-- for each valid dataset release from the processing center
        drel = [r for r in DREL if r in VALID[p]]
        for r in drel:
            #-- for number of data products
            for d in DSET[p][r]:
                logging.info('GRACE Date Program: {0} {1} {2}'.format(p,r,d))
                #-- run program for processing center, data release and product
                grace_date(base_dir,PROC=p,DREL=r,DSET=d,OUTPUT=True,MODE=MODE)

    #-- run grace months program for data releases
    logging.info('GRACE Months Program')
    grace_months_index(base_dir, DREL=DREL, MODE=MODE)


#-- PURPOSE: program that calls run_grace_date() with set parameters
def main():
    #-- command line parameters
    #-- Read the system arguments listed after the program
    parser = argparse.ArgumentParser(
        description="""Wrapper program for running GRACE date and
            months programs
            """
    )
    #-- working data directory
    parser.add_argument('--directory','-D',
        type=lambda p: os.path.abspath(os.path.expanduser(p)),
        default=os.getcwd(),
        help='Working data directory')
    #-- Data processing center or satellite mission
    parser.add_argument('--center','-c',
        metavar='PROC', type=str, nargs='+',
        default=['CSR','GFZ','JPL'],
        choices=['CSR','GFZ','JPL'],
        help='GRACE/GRACE-FO Processing Center')
    #-- GRACE/GRACE-FO data release
    parser.add_argument('--release','-r',
        metavar='DREL', type=str, nargs='+',
        default=['RL06','v02.4'],
        help='GRACE/GRACE-FO Data Release')
    #-- print information about each input and output file
    parser.add_argument('--verbose','-V',
        default=False, action='store_true',
        help='Verbose output of run')
    #-- permissions mode of the local directories and files (number in octal)
    parser.add_argument('--mode','-M',
        type=lambda x: int(x,base=8), default=0o775,
        help='permissions mode of output files')
    args,_ = parser.parse_known_args()

    #-- run GRACE preliminary date program
    run_grace_date(args.directory, args.center, args.release,
        VERBOSE=args.verbose, MODE=args.mode)

#-- run main program
if __name__ == '__main__':
    main()
