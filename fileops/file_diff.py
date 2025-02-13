#!/usr/bin/python3
#
# Output the diff of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the entire line from the left file
#
# Usage:
#   python file_diff.py [options] left_file right_file

import os
import sys
import csv
import argparse
from collections import OrderedDict
from typing import List, Dict, Any

from . import csv_unicode, file_ops_common


def process_file_diff(left_file: str, right_file: str, left_columns: str = '0',
                     right_columns: str = '0', left_delim: str = '\t',
                     right_delim: str = '\t', lower_case: bool = False) -> List[List[str]]:
    """Process the diff between two files based on specified columns.
    
    Args:
        left_file: Path to the left file
        right_file: Path to the right file
        left_columns: Comma-separated string of column indices for left file
        right_columns: Comma-separated string of column indices for right file
        left_delim: Delimiter for left file
        right_delim: Delimiter for right file
        lower_case: Whether to ignore case when comparing
        
    Returns:
        List of rows that are in left_file but not in right_file
    """
    left_key_cols = [int(col) for col in left_columns.split(',')]
    right_key_cols = [int(col) for col in right_columns.split(',')]

    # We use an ordered dict to maintain the original order of the lines
    all_keys: Dict[str, List[List[str]]] = OrderedDict()

    # Go through the left file and collect the keys
    with open(left_file, 'r', encoding='utf-8') as f:
        for cols in csv_unicode.UnicodeReader(f, delimiter=left_delim):
            key = file_ops_common.get_key(cols, left_key_cols)
            if lower_case:
                key = key.lower()
            if key not in all_keys:
                all_keys[key] = []
            all_keys[key].append(cols)

    # Go through the right file and remove those keys from all_keys
    with open(right_file, 'r', encoding='utf-8') as f:
        for cols in csv_unicode.UnicodeReader(f, delimiter=right_delim):
            key = file_ops_common.get_key(cols, right_key_cols)
            if lower_case:
                key = key.lower()
            if key in all_keys:
                all_keys.pop(key, None)

    # Return the remaining rows
    result = []
    for key in all_keys:
        for line in all_keys[key]:
            result.append(line)
    return result


def main() -> None:
    """Output the diff of 2 files, based on certain columns in the files.
    Loads the keys in memory, so only works on small/medium sized files.
    It outputs the entire line from the left file"""

    parent_argparser = file_ops_common.set_ops_parser()
    argparser = argparse.ArgumentParser(description=main.__doc__,
                                      parents=[parent_argparser])
    args = argparser.parse_args()

    result = process_file_diff(
        args.left_file,
        args.right_file,
        args.left_columns,
        args.right_columns,
        args.left_delim,
        args.right_delim,
        args.lower_case
    )

    # Output the results
    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=args.left_delim)
    for line in result:
        output.writerow(line)


if __name__ == '__main__':
    main()
