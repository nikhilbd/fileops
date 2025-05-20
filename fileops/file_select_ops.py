#!/usr/bin/python
#
# Do SQL-like operations on a delimited files.
# E.g. SELECT col0, col1, SUM(col2)
#      FROM file1.txt
#      WHERE col0 NOT IN ("c") AND col1 IN ("a","b")
#      GROUP BY col0, col1
# Currently supported aggregate operations: SUM & COUNT
#

import os, sys, csv, argparse
from . import csv_unicode, file_ops_common
from collections import defaultdict, OrderedDict


def print_query(args, select_cols, aggregate_cols, where_filters):
    where_print = []
    for col in where_filters.keys():
        where_print.append('col%d %s (' % (col, where_filters[col]['op']) +
                           ', '.join('"%s"' % val for val in where_filters[col]['vals']) +
                           ')')

    select_cols_print = ', '.join(['col' + str(col) for col in select_cols])

    sys.stderr.write('\nYour query:\n' +
      'SELECT ' + select_cols_print + ', ' +
      ', '.join(['%s(col%s)' % (args.agg_function, col) for col in aggregate_cols]) +
      '\nFROM ' + args.file +
      '\nWHERE ' + ' AND '.join(where_print) +
      '\nGROUP BY ' + select_cols_print + '\n\n')

def process_select_operations(input_file_path: str, select_cols_str: str,
                              aggregate_cols_str: str, agg_function: str,
                              where_clauses_list: list, delimiter_char: str) -> list:
    # Parse the where clause
    where_filters = {}
    if where_clauses_list:
        for clause in where_clauses_list:
            if '!=' in clause:
                clause_parts = clause.split('!=')
                where_filters[int(clause_parts[0])] = {
                  'op' : 'NOT IN',
                  'vals' : clause_parts[1].split(',')
                }
            elif '=' in clause:
                clause_parts = clause.split('=')
                where_filters[int(clause_parts[0])] = {
                  'op' : 'IN',
                  'vals' : clause_parts[1].split(',')
                }

    select_cols = [int(col) for col in select_cols_str.split(',')]
    aggregate_cols = [int(col) for col in aggregate_cols_str.split(',')]

    # The structure where we save the aggregated values
    # It is a nested dictionary for the form:
    # Select Keys -> Aggregate Column -> Aggregate value
    aggregates = {}

    # Go through the input file and do the aggregation
    with open(input_file_path, 'r') as infile:
        reader = csv_unicode.UnicodeReader(infile, delimiter=delimiter_char)
        next(reader, None)  # Skip header row
        for cols in reader:
            # Where filters
            skip = False
            for col_num, filtr in where_filters.items():
                if ((filtr['op'] == 'IN' and cols[col_num] not in filtr['vals']) or
                    (filtr['op'] == 'NOT IN' and cols[col_num] in filtr['vals'])):
                    skip = True
                    break
            if skip:
                continue

            # Generate the key from the select columns
            key = file_ops_common.get_key(cols, select_cols)
            if key not in aggregates: aggregates[key] = defaultdict(int)

            # Go over each aggregate column and add it to the final structure
            for col_num in aggregate_cols:
                if agg_function == 'sum':
                    aggregates[key][col_num] += float(cols[col_num])
                elif agg_function == 'count':
                    aggregates[key][col_num] += 1
                else:
                    sys.stderr.write('Invalid aggregate function: ' + agg_function)
                    sys.exit(-1)
    
    output_rows = []
    # Output the remaining keys
    for key in aggregates:
        op_cols = file_ops_common.split_key(key)
        # We output the aggregate column in the order they are in the input file
        for col, value in sorted(aggregates[key].items()):
            op_cols += [str(value)]
        output_rows.append(op_cols)
    return output_rows

def main():
    ''' Do SQL-like operations on a delimited text file'''

    args = parse_args()

    # Parse the where clause for print_query
    where_filters = {}
    if args.where_clauses:
        for clause in args.where_clauses:
            if '!=' in clause:
                clause_parts = clause.split('!=')
                where_filters[int(clause_parts[0])] = {
                  'op' : 'NOT IN',
                  'vals' : clause_parts[1].split(',')
                }
            elif '=' in clause:
                clause_parts = clause.split('=')
                where_filters[int(clause_parts[0])] = {
                  'op' : 'IN',
                  'vals' : clause_parts[1].split(',')
                }
    
    select_cols_int = [int(col) for col in args.select_cols.split(',')]
    aggregate_cols_int = [int(col) for col in args.aggregate_cols.split(',')]

    if args.verbose:
        # print_query expects args for file and agg_function, 
        # but parsed lists/dicts for select_cols, aggregate_cols, and where_filters
        print_query(args, select_cols_int, aggregate_cols_int, where_filters)

    output_rows = process_select_operations(args.file, args.select_cols,
                                            args.aggregate_cols, args.agg_function,
                                            args.where_clauses, args.delim)

    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=args.delim)
    for row in output_rows:
        output.writerow(row)


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass

def parse_args():
    desc = 'Do SQL-like operations on a delimited files. Currently supported '
    'aggregate operations: SUM & COUNT.'

    epilog = '''Example:

file_select_ops.py --select-cols="0,1" --aggregate-cols=2 --aggregate-function=sum
  --where-clauses 0!=c 1=a,b file1.txt

This is equivalent to the following SQL statement

SELECT col0, col1, SUM(col2)
FROM file1.txt
WHERE col0 NOT IN ("c") AND col1 IN ("a","b")
GROUP BY col0, col1'''

    parser = argparse.ArgumentParser(formatter_class=CustomFormatter,
                                     description=desc, epilog=epilog)

    parser.add_argument('file', help='Delimited input file')
    parser.add_argument('-s', '--select-cols', dest='select_cols',
                        default='0', help='List of column numbers from the input file to'
                        ' SELECT & GROUP BY on. E.g. "0,1,5"')
    parser.add_argument('-a', '--aggregate-cols', dest='aggregate_cols',
                        default='1', help='List of column numbers from the input file to '
                        'run the aggregate function on. E.g. "1,5"')
    parser.add_argument('-d', '--delim', dest='delim', default='\t',
                        help='Delimiter for the input & output files. E.g. ",".')
    parser.add_argument('-f', '--aggregate_function', dest='agg_function',
                        choices=['sum', 'count'],
                        default='sum',
                        help='Aggregate function. Needs to be either "sum" or "count".')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose')
    parser.add_argument(
        '-w', '--where-clauses', dest='where_clauses', nargs='*',
        help='''Where clauses for the query.
        E.g. "1=text1,text2" translates to WHERE col1 IN ("text1","text2").
        "3!=text5,text6" translates to WHERE col3 NOT IN ("text5","text6").
        You can specify multiple of these. They will be joined with an AND.
        If present, this should be the last argument in your command!''')

    args = parser.parse_args()

    args.agg_function = args.agg_function.lower()

    return args

if __name__ == '__main__':
    main()
