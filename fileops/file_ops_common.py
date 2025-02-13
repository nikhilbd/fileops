#!/usr/bin/python3
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# A bunch of common operations for the file set operations scripts
# like file_intersection.py, file_diff.py etc.
#

import os
import sys
import csv
import argparse
from typing import List, Union, TextIO

from . import csv_unicode


def set_ops_parser() -> argparse.ArgumentParser:
    ''' Common arguments for the file_diff and the file_intersection scripts '''

    parser = argparse.ArgumentParser(add_help=False,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('left_file', help='Left input file')
    parser.add_argument('right_file', help='Right input file')
    parser.add_argument('-i', '--ignore_case', dest='lower_case',
                        action='store_true', help='Ignore the case for the key'
                        ' columns')
    parser.add_argument('-l', '--left-columns', dest='left_columns',
                        default='0', help='List of column numbers from the left file to'
                        'intersect on. E.g. "0,1,5"')
    parser.add_argument('-r', '--right-columns', dest='right_columns',
                        default='0', help='List of column numbers from the right file to'
                        'intersect on. E.g. "0,1,5"')
    parser.add_argument('--left-delim', dest='left_delim', default='\t',
                        help='Delimiter for the left file. E.g. ","')
    parser.add_argument('--right-delim', dest='right_delim', default='\t',
                        help='Delimiter for the right file. E.g. ","')

    return parser

KEY_DELIMITER='\t'
def get_key(cols: List[str], key_cols: List[int]) -> str:
    key = cols[key_cols[0]]
    for i in range(1, len(key_cols)):
        key += KEY_DELIMITER + cols[key_cols[i]]
    return key

def split_key(key: str) -> List[str]:
    return key.split(KEY_DELIMITER)
