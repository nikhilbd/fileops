#!/usr/bin/python
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# A bunch of common operations for the file set operations scripts
# like file_intersection.py, file_diff.py etc.
#

import os, sys, csv_unicode, csv, optparse

def parse_args(description, is_intersect_script = False):
    usage = 'usage: <script_name> [options] left_file right_file'

    parser = optparse.OptionParser(usage=usage, description=description)

    parser.add_option('-i', '--ignore_case', dest='lower_case',
                      action='store_true', help='Ignore the case for the key'
                      ' columns')
    parser.add_option('--left-columns', dest='left_columns',
                      default='0', help='List of columns in the left file to'
                      'intersect on. E.g. "0,1,5"')
    parser.add_option('--right-columns', dest='right_columns',
                      default='0', help='List of columns in the right file to'
                      'intersect on. E.g. "0,1,5"')
    parser.add_option('--left-delim', dest='left_delim', default='\t',
                      help='Delimiter for the left file. E.g. ","')
    parser.add_option('--right-delim', dest='right_delim', default='\t',
                      help='Delimiter for the right file. E.g. ","')

    if is_intersect_script:
        parser.add_option('--insert-cols', dest='insert_cols', default='',
                          help='Columns from the right file to insert into the left.'
                          ' If there are multiple rows matching from the right file, we'
                          ' only consider the 1st match row')

    (opts, args) = parser.parse_args()
    if len(args) != 2:
        parser.error('You need to provide the left & right files as inputs')
    return (opts, args)

KEY_DELIMITER='\t'
def get_key(cols, key_cols):
    key = cols[key_cols[0]]
    for i in range(1, len(key_cols)):
        key += KEY_DELIMITER + cols[key_cols[i]]
    return key

def split_key(key):
    return key.split(KEY_DELIMITER)
