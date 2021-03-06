fileops
====================

Useful command line scripts for file operations. Here are the supported operations

### 1. File intersection
Intersection of 2 files using a subset of columns in the files as intersection keys. This is equivalent to the SQL INNER JOIN operation
##### Usage
    python file_intersection.py [options] left_file right_file

##### Example
Given *file1.txt* as

    a,1,apple
    a,3,adam
    b,2,boy
    c,3,catch
    d,4,dog
    b,15,boy

and *file2.txt* as

    b,2,bat
    d,4,donkey
    e,5,elephant   

you can do
  
    python file_intersection.py --left-delim=, --right-delim=, file.txt file2.txt
    b,2,boy
    b,15,boy
    d,4,dog
    
Additional options let you select the *key* columns on both files, allow you to insert certain columns from the *right* file into your output etc.

### 2. File difference
Difference between 2 files using a subset of columns in the files as keys.
##### Usage
    python file_diff.py [options] left_file right_file

##### Example
    
    python file_diff.py --left-delim=, --right-delim=, file.txt file2.txt
    a,1,apple
    a,3,adam
    c,3,catch

Additional options let you select the *key* columns on both files

### 3. SQL-like operation on a delimited file
Lets you do a SQL-like SELECT/WHERE/GROUP BY aggregate operation on a file with columnar data. 

##### Usage
    python file_select_ops.py [options] input_file
    
##### Example

    file_select_ops.py --select-cols="0,2" --aggregate-cols=1 --aggregate-function=sum --delim=, file1.txt --where-clauses "0=a,b" "2!=adam,catch" 

is equivalent to the following SQL statement    

    SELECT col0, col2, sum(col1)
    FROM file1.txt
    WHERE col0 IN ("a", "b") AND col2 NOT IN ("adam", "catch")
    GROUP BY col0, col2

and will produce the following output for the file1.txt described in the 1st example

    a,apple,1.0
    b,boy,17.0

You should specify the *verbose* option to print the SQL query equivalent to your passed parameters

### 4. Prefix search in a file
Search within a *sorted* file using a string prefix

##### Usage
    python file_searcher.py filename search_string

##### Example

For file2.txt from the 1st example (as you can see file2.txt is already sorted):

    > ./file_searcher.py file2.txt b
    b,2,bat
    >
    > ./file_searcher.py file2.txt "d,4"
    d,4,donkey
    > ./file_searcher.py file2.txt "d,10"
    >
    
