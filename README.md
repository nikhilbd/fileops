fileops
====================

Useful command line scripts for file operations. Here are the supported operations

**Note:** Input files are generally expected to be UTF-8 encoded, especially for scripts processing text content like `file_searcher.py`.

## Running Tests
Tests for this project are run using `pytest`.

To install the necessary dependencies for running tests, use the following command:
```bash
pip install -e .[test]
```

Once dependencies are installed, you can run the tests with:
```bash
pytest
```

### 1. File intersection
Intersection of 2 files using a subset of columns in the files as intersection keys. This is equivalent to the SQL INNER JOIN operation. The script outputs columns from the *left* file, which can be optionally augmented with columns from the *right* file using the `--insert-cols` option.
##### Usage
    python file_intersection.py [options] left_file right_file

##### Example
Given *file1.txt* as (comma-delimited):

    a,1,apple,red
    a,3,adam,blue
    b,2,boy,green
    c,3,catch,yellow
    d,4,dog,black
    b,15,boy,white

and *file2.txt* as (comma-delimited):

    b,2,bat,round
    d,4,donkey,tall
    e,5,elephant,large

To find the intersection based on the first two columns of *file1.txt* and *file2.txt*, and include the third column from *file2.txt* in the output:

    python file_intersection.py --left-columns=0,1 --right-columns=0,1 --insert-cols=2 file1.txt file2.txt
    b,2,boy,green,bat
    d,4,dog,black,donkey

The default delimiter is tab. If your files are comma-delimited as in the example, you would add `--left-delim=, --right-delim=,`.

The script also supports case-insensitive comparison with the `--ignore_case` option.

### 2. File difference
Difference between 2 files using a subset of columns in the files as keys. The script outputs lines from the *left* file that are not present in the *right* file, based on the specified key columns.
##### Usage
    python file_diff.py [options] left_file right_file

##### Example
Given *file1.txt* as (comma-delimited):

    a,1,apple,red
    a,3,adam,blue
    b,2,boy,green
    c,3,catch,yellow
    d,4,dog,black
    b,15,boy,white

and *file2.txt* as (comma-delimited):

    b,2,bat,round
    d,4,donkey,tall
    e,5,elephant,large

To find lines in *file1.txt* that are not in *file2.txt*, based on the first two columns:

    python file_diff.py --left-columns=0,1 --right-columns=0,1 file1.txt file2.txt
    a,1,apple,red
    a,3,adam,blue
    c,3,catch,yellow
    b,15,boy,white

The default delimiter is tab. If your files are comma-delimited as in the example, you would add `--left-delim=, --right-delim=,`.

The script also supports case-insensitive comparison with the `--ignore_case` option.

### 3. SQL-like operation on a delimited file
Lets you do a SQL-like SELECT/WHERE/GROUP BY aggregate operation on a file with columnar data.
**Note:** This script assumes the first line of the input file is a header and skips it.

##### Usage
    python file_select_ops.py [options] input_file
    
##### Example
Given *file1.txt* as (comma-delimited):

    name,value,fruit,color
    a,1,apple,red
    a,3,adam,blue
    b,2,boy,green
    c,3,catch,yellow
    d,4,dog,black
    b,15,boy,white

To select the 'name' (column 0) and 'fruit' (column 2), sum the 'value' (column 1), grouping by 'name' and 'fruit', for rows where 'name' is 'a' or 'b' AND 'fruit' is not 'adam' or 'catch':

    python file_select_ops.py --select-cols="0,2" --aggregate-cols=1 --aggregate-function=sum --delim=, file1.txt --where-clauses "0=a,b" "2!=adam,catch"

This is equivalent to the following SQL statement:

    SELECT col0, col2, sum(col1)
    FROM file1.txt
    WHERE col0 IN ('a', 'b') AND col2 NOT IN ('adam', 'catch')
    GROUP BY col0, col2

Output:

    a,apple,1.0
    b,boy,17.0

The `--where-clauses` option accepts multiple arguments. Each argument is a string defining a condition, e.g., `"column_index=value1,value2"` or `"column_index!=value3"`.

Use the `-v` or `--verbose` option to print the SQL query equivalent to your passed parameters.

### 4. Prefix search in a file
Search within a *sorted* file using a string prefix.
**Note:** The input file must be sorted for this script to work correctly. It is also assumed to be UTF-8 encoded.

##### Usage
    python file_searcher.py filename search_string

##### Example
Given *file2.txt* as (comma-delimited and sorted):

    b,2,bat,round
    d,4,donkey,tall
    e,5,elephant,large

    > python file_searcher.py file2.txt b
    b,2,bat,round
    >
    > python file_searcher.py file2.txt "d,4"
    d,4,donkey,tall
    > python file_searcher.py file2.txt "d,10"
    >
