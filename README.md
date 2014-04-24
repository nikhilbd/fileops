command-line-scripts
====================

Useful command line scripts

### 1. File intersection
Intersection of 2 files using arbitrary columns in the files.
##### Usage
    python file_intersection.py -h

### 2. File difference
Difference between 2 files using arbitrary columns in the files.
##### Usage
    python file_diff.py -h

### 3. Prefix search in a file
Search within a sorted file using a string prefix
##### Usage
    python file_searcher.py -h
    
### 4. SQL-like operation on a delimited file
E.g. "SELECT col1, col2, SUM(col3), SUM(col4)
      WHERE col1 IN ("X", "Y") AND col2 != "Z"
      GROUP BY col1, col2
##### Usage
    python file_select_ops.py -h
    
    

 
