fileops
====================

Useful command line scripts for file operations. Here are the supported operations

### 1. File intersection
Intersection of 2 files using a subset of columns in the files as intersection keys. This is equivalent to the SQL INNER JOIN operation
##### Usage
    python file_intersection.py [options] left_file right_file

###### Example
Given *file1.txt* as

    a,1,apple
    b,2,boy
    c,3,catch
    d,4,dog

and *file2.txt* as

    b,2,bat
    d,4,donkey
    e,5,elephant

    python file_intersection.py --left-delim=, --right-delim=, file.txt file2.txt
    b,2,boy
    d,4,dog
    

### 2. File difference
Difference between 2 files using a subset of columns in the files as keys.
##### Usage
    python file_diff.py [options] left_file right_file

### 3. SQL-like operation on a delimited file
E.g. "SELECT col1, col2, SUM(col3), SUM(col4)
      WHERE col1 IN ("X", "Y") AND col2 != "Z"
      GROUP BY col1, col2
##### Usage
    python file_select_ops.py -h

### 3. Prefix search in a file
Search within a sorted file using a string prefix
##### Usage
    python file_searcher.py -h
    
    
    

 
