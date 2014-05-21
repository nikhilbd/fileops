#!/usr/bin/python
#
# Output the diff of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the entire line from the left file
#
# Usage:
#   python file_diff.py [options] left_file right_file

import os, sys, csv_unicode, csv, argparse, file_ops_common
from collections import OrderedDict

def main():
    '''Output the diff of 2 files, based on certain columns in the files.
    Loads the keys in memory, so only works on small/medium sized files.
    It outputs the entire line from the left file'''

    parent_argparser = file_ops_common.set_ops_parser()
    argparser = argparse.ArgumentParser(description=main.__doc__,
                                        parents=[parent_argparser])
    args = argparser.parse_args()

    left_key_cols = [int(col) for col in args.left_columns.split(',')]
    right_key_cols = [int(col) for col in args.right_columns.split(',')]

    # We use an ordered dict to maintain the original order of the lines
    all_keys = OrderedDict()

    # Go through the left file and collect the keys
    for cols in csv_unicode.UnicodeReader(open(args.left_file, 'r'),
                                          delimiter=args.left_delim):
        key = file_ops_common.get_key(cols, left_key_cols)
        if args.lower_case: key = key.lower()
        if key not in all_keys:
            all_keys[key] = []
        all_keys[key].append(cols)

    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=args.left_delim)

    # Go through the right file and remove those keys from all_keys
    for cols in csv_unicode.UnicodeReader(open(args.right_file, 'r'),
                                          delimiter=args.right_delim):
        key = file_ops_common.get_key(cols, right_key_cols)
        if args.lower_case: key = key.lower()
        if key in all_keys:
            all_keys.pop(key, None)

    # Output the remaining keys
    for key in all_keys:
        for line in all_keys[key]:
            output.writerow(line)

if __name__ == '__main__':
    main()
