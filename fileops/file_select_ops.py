#!/usr/bin/python
#
# Do SQL-like operations on a delimited files.
# E.g. SELECT col1, col2, SUM(col3), SUM(col4)
#      WHERE col1 IN ('X', 'Y') AND col2 != 'Z'
#      GROUP BY col1, col2
# Currently supported aggregate operations: SUM & COUNT
#
# Usage:
#  python file_select_ops.py [options] input_file

import os, sys, csv_unicode, csv, optparse, file_ops_common
from collections import defaultdict, OrderedDict

def main():
    ''' Do SQL-like operations on a delimited text file'''

    (opts, args) = parse_args()

    # Parse the where clause
    where_filters = {}
    if opts.where_clauses:
        clauses = opts.where_clauses.split(';')
        for clause in clauses:
            if '!=' in clause:
                clause_parts = clause.split('!=')
                where_filters[int(clause_parts[0])] = {
                  'op' : '!=',
                  'vals' : clause_parts[1].split(',')
                }
            elif '=' in clause:
                clause_parts = clause.split('=')
                where_filters[int(clause_parts[0])] = {
                  'op' : '=',
                  'vals' : clause_parts[1].split(',')
                }

    select_cols = [int(col) for col in opts.select_cols.split(',')]
    aggregate_cols = [int(col) for col in opts.aggregate_cols.split(',')]

    if opts.verbose:
        sys.stderr.write('Your query:\n' +
          'select ' + opts.select_cols + ',' +
          ', '.join(['%s(%s)' % (opts.agg_function, col) for col in aggregate_cols]) +
          '\n group by ' + opts.aggregate_cols)
        sys.stderr.write('\nWhere clause : ' + str(where_filters) + '\n')

    # The structure where we save the aggregated values
    # It is a nested dictionary for the form:
    # Select Keys -> Aggregate Col -> Aggregate value
    aggregates = {}

    # Go through the input file and do the aggregation
    for cols in csv_unicode.UnicodeReader(open(args[0], 'r'),
                                          delimiter=opts.delim):

        # Where filters
        skip = False
        for col_num, filtr in where_filters.iteritems():
            if ((filtr['op'] == '=' and cols[col_num] not in filtr['vals']) or
                (filtr['op'] == '!=' and cols[col_num] in filtr['vals'])):
                skip = True
                break
        if skip:
            continue

        # Generate the key from the select columns
        key = file_ops_common.get_key(cols, select_cols)
        if key not in aggregates: aggregates[key] = defaultdict(int)

        # Go over each aggregate column and add it to the final structure
        for col_num in aggregate_cols:
            if opts.agg_function == 'sum':
                aggregates[key][col_num] += float(cols[col_num])
            elif opts.agg_function == 'count':
                aggregates[key][col_num] += 1
            else:
                sys.stderr.write('Invalid aggregate function: ' + opts.agg_function)
                sys.exit(-1)

    output = csv_unicode.UnicodeWriter(sys.stdout, delimiter=opts.delim)

    # Output the remaining keys
    for key in aggregates:
        op_cols = key.split('\t')
        # We output the aggregate column in the order they are in the input file
        for col, value in sorted(aggregates[key].items()):
            op_cols += [unicode(value)]
        output.writerow(op_cols)

def parse_args():
    desc = '''Do SQL-like operations on a delimited files.
    E.g. you can do operations equivalent to
    "SELECT col1, col2, SUM(col3), SUM(col4)
    WHERE col1 IN ("X", "Y") AND col2 != "Z"
    GROUP BY col1, col2"
    Currently supported aggregate operations: SUM & COUNT'''

    usage = 'Usage: python %s [options] input_file' % (
      os.path.basename(__file__))
    parser = optparse.OptionParser(usage=usage, description=desc)

    parser.add_option('-s', '--select-cols', dest='select_cols',
                      default='0', help='List of columns in the input file to'
                      ' SELECT & GROUP BY on. E.g. "0,1,5". Default "0"')
    parser.add_option('-a', '--aggregate-cols', dest='aggregate_cols',
                      default='1', help='List of columns in the input file to '
                      'run the aggregate function on. E.g. "1,5". Default="1"')
    parser.add_option(
        '-w', '--where-clauses', dest='where_clauses',
        help='Where clauses for the query. The format is "1=text1,text2;3!=text5".'
        ' This translates to '
        'WHERE col1 IN ("text1","text2") AND col3 != "text3"')
    parser.add_option('-d', '--delim', dest='delim', default='\t',
                      help='Delimiter for the input & output files. E.g. ",".'
                      ' Default=$"\\t"')
    parser.add_option('-f', '--aggregate_function', dest='agg_function',
                      default='SUM',
                      help='Aggregate function. Needs to be either SUM or COUNT. '
                      'Default=SUM')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')

    (opts, args) = parser.parse_args()

    opts.agg_function = opts.agg_function.lower()

    if len(args) != 1 and (opts.agg_function != 'sum' or
                           opts.agg_function != 'count'):
        parser.error('Invalid arguments! ')
    return (opts, args)


if __name__ == '__main__':
    main()
