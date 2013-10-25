#!/usr/bin/python
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# Output the intersection of 2 files, based on certain columns in the files
# Loads the keys in memory, so only works on small/medium sized files
# It outputs the full lines from the left file
#
# Usage:
#   file_intersection.py -h

import os, sys, csv_unicode, csv, optparse

def parse_args():
  usage = os.path.basename(__file__) + ' -h'
  parser = optparse.OptionParser(usage=usage)

  parser.add_option('-l', '--left_file', dest='left_file',
                    help='Left file')
  parser.add_option('-r', '--right_file', dest='right_file',
                    help='Right file')
  parser.add_option('-o', '--output_file', dest='output_file',
                    help='Output file')
  parser.add_option('-c', '--columns', dest='columns',
                    default='0',
                    help='List of columns to intersect on. E.g. "0,1,5"')
  parser.add_option('-i', '--ignore_case', dest='lower_case',
                    action='store_true', help='Ignore the case for the key'
                    ' columns')

  (opts, args) = parser.parse_args()
  if not (opts.left_file and opts.right_file and
          opts.output_file):
    print usage
    sys.exit(-1)
  return opts

def get_key(cols, key_cols):
  key = cols[key_cols[0]]
  for i in range(1, len(key_cols)):
    key += '\t' + cols[key_cols[i]]
  return key

def main():
  opts = parse_args()

  key_cols = [int(col) for col in opts.columns.split(',')]

  # Go through the left file and collect the keys
  all_keys = dict()
  for cols in csv_unicode.UnicodeReader(open(opts.left_file, 'r'),
                                        delimiter='\t'):
    key = get_key(cols, key_cols)
    if opts.lower_case: key = key.lower()
    if key not in all_keys:
      all_keys[key] = []
    all_keys[key].append(cols)

  output = csv_unicode.UnicodeWriter(open(opts.output_file, 'w'), delimiter='\t')

  # Right file
  for cols in csv_unicode.UnicodeReader(open(opts.right_file, 'r'),
                                        delimiter='\t'):
    key = get_key(cols, key_cols)
    if opts.lower_case: key = key.lower()
    if key in all_keys:
      for line in all_keys[key]:
        output.writerow(line)

if __name__ == '__main__':
  main()
