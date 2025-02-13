#!/usr/bin/python3
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# Output the intersection of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the full lines from the left file, optionally adding lines from
# the right file into it
#
# Usage:
#   python file_intersection.py [options] left_file right_file

import os
import sys
import csv
import argparse
from typing import List, Dict, Any

from . import csv_unicode, file_ops_common


def process_file_intersection(left_file: str, right_file: str, left_columns: str = '0',
                            right_columns: str = '0', left_delim: str = '\t',
                            right_delim: str = '\t', lower_case: bool = False,
                            insert_cols: str = '') -> List[List[str]]:
    """Process the intersection between two files based on specified columns.
    
    Args:
        left_file: Path to the left file
        right_file: Path to the right file
        left_columns: Comma-separated string of column indices for left file
        right_columns: Comma-separated string of column indices for right file
        left_delim: Delimiter for left file
        right_delim: Delimiter for right file
        lower_case: Whether to ignore case when comparing
        insert_cols: Comma-separated string of column indices from right file to insert
        
    Returns:
        List of rows that are in both files, with optional columns from right file
    """
    left_key_cols = [int(col) for col in left_columns.split(',')]
    right_key_cols = [int(col) for col in right_columns.split(',')]
    insert_cols_list = [int(col) for col in insert_cols.split(',')] if insert_cols else []

    # Go through the left file and collect the keys
    all_keys: Dict[str, List[List[str]]] = {}
    with open(left_file, 'r', encoding='utf-8') as f:
        for cols in csv_unicode.UnicodeReader(f, delimiter=left_delim):
            key = file_ops_common.get_key(cols, left_key_cols)
            if lower_case:
                key = key.lower()
            if key not in all_keys:
                all_keys[key] = []
            all_keys[key].append(cols)

    # Process right file and build result
    result = []
    with open(right_file, 'r', encoding='utf-8') as f:
        for cols in csv_unicode.UnicodeReader(f, delimiter=right_delim):
            key = file_ops_common.get_key(cols, right_key_cols)
            if lower_case:
                key = key.lower()
            if key in all_keys:
                for line in all_keys[key]:
                    insert_values = [cols[i] for i in insert_cols_list]
                    result.append(line + insert_values)
                all_keys.pop(key)

    return result


def main() -> None:
    """Output the intersection of 2 files, based on certain columns in the
    files. This is equivalent to the SQL JOIN operation. Loads the keys in memory,
    so only works on small/medium sized files. It outputs the full lines from the
    left file, optionally adding columns from the right file into it"""

    parent_argparser = file_ops_common.set_ops_parser()
    argparser = argparse.ArgumentParser(description=main.__doc__,
                                      parents=[parent_argparser])
    argparser.add_argument('--insert-cols', dest='insert_cols', default='',
                          help='Columns from the right file to insert into the left.'
                          ' If there are multiple rows matching from the right file, we'
                          ' only consider the 1st match row')
    args = argparser.parse_args()

    result = process_file_intersection(
        args.left_file,
        args.right_file,
        args.left_columns,
        args.right_columns,
        args.left_delim,
        args.right_delim,
        args.lower_case,
        args.insert_cols
    )

    # Output the results
    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=args.left_delim)
    for line in result:
        output.writerow(line)


if __name__ == '__main__':
    main()
