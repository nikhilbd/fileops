#!/usr/bin/python
#
# Output the diff of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the entire line from the left file
#
# Usage:
#   python file_diff.py [options] left_file right_file

import os, sys, csv_unicode, csv, optparse, file_ops_common
from collections import OrderedDict

def main():
  '''Output the diff of 2 files, based on certain columns in the files.
Loads the keys in memory, so only works on small/medium sized files.
It outputs the entire line from the left file'''

  (opts, args) = file_ops_common.parse_args(main.__doc__)

  left_key_cols = [int(col) for col in opts.left_columns.split(',')]
  right_key_cols = [int(col) for col in opts.right_columns.split(',')]

  # We use an ordered dict to maintain the original order of the lines
  all_keys = OrderedDict()

  # Go through the left file and collect the keys
  for cols in csv_unicode.UnicodeReader(open(args[0], 'r'),
                                        delimiter=opts.left_delim):
    key = file_ops_common.get_key(cols, left_key_cols)
    if opts.lower_case: key = key.lower()
    if key not in all_keys:
      all_keys[key] = []
    all_keys[key].append(cols)

  output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=opts.left_delim)

  # Go through the right file and remove those keys from all_keys
  for cols in csv_unicode.UnicodeReader(open(args[1], 'r'),
                                        delimiter=opts.right_delim):
    key = file_ops_common.get_key(cols, right_key_cols)
    if opts.lower_case: key = key.lower()
    if key in all_keys:
      all_keys.pop(key, None)

  # Output the remaining keys
  for key in all_keys:
    for line in all_keys[key]:
      output.writerow(line)

if __name__ == '__main__':
  main()
