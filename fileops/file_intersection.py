#!/usr/bin/python
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# Output the intersection of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the full lines from the left file, optionally adding lines from
# the right file into it
#
# Usage:
#   python file_intersection.py [options] left_file right_file

import os, sys, csv_unicode, csv, argparse, file_ops_common

def main():
    '''Output the intersection of 2 files, based on certain columns in the
    files. This is equivalent to the SQL JOIN operation. Loads the keys in memory,
    so only works on small/medium sized files. It outputs the full lines from the
    left file, optionally adding columns from the right file into it'''

    parent_argparser = file_ops_common.set_ops_parser()
    argparser = argparse.ArgumentParser(description=main.__doc__,
                                        parents=[parent_argparser])
    argparser.add_argument('--insert-cols', dest='insert_cols', default='',
                           help='Columns from the right file to insert into the left.'
                           ' If there are multiple rows matching from the right file, we'
                           ' only consider the 1st match row')
    args = argparser.parse_args()

    left_key_cols = [int(col) for col in args.left_columns.split(',')]
    right_key_cols = [int(col) for col in args.right_columns.split(',')]
    insert_cols = [int(col) for col in args.insert_cols.split(',')] if (
        args.insert_cols) else []

    # Go through the left file and collect the keys
    all_keys = dict()
    for cols in csv_unicode.UnicodeReader(open(args.left_file, 'r'),
                                          delimiter=args.left_delim):
        key = file_ops_common.get_key(cols, left_key_cols)
        if args.lower_case: key = key.lower()
        if key not in all_keys:
            all_keys[key] = []
        all_keys[key].append(cols)

    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=args.left_delim)

    # Right file
    for cols in csv_unicode.UnicodeReader(open(args.right_file, 'r'),
                                          delimiter=args.right_delim):
        key = file_ops_common.get_key(cols, right_key_cols)
        if args.lower_case: key = key.lower()
        if key in all_keys:
            for line in all_keys[key]:
                insert_values = [cols[i] for i in insert_cols]
                line = line + insert_values
                output.writerow(line)
            all_keys.pop(key)

if __name__ == '__main__':
    main()
