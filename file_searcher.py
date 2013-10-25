#!/usr/bin/python
#
# Binary search within a large sorted file by columns
# Assumes the file is in unicode
#
# Usage:
# s = Searcher('file_path')
# s.find('test string')
#

import codecs, sys


class Searcher:
    """
    Prefix search for a string in a sorted file

    Usage:
    s = Searcher('file_path')
    s.find('test string')
    """

    def __init__(self, filename):
        self.file = codecs.open(filename, 'rb', encoding='utf-8')
        self.file.seek(0,2)
        self.length = self.file.tell()

    # This does a binary search, with a slight modification of running
    # down to the previous line-break, so that it can read the complete
    # line
    def find(self, string, verbose = False):
        low = 0
        high = self.length

        while low < high:
            mid = (low + high) // 2
            p = mid
            self._seek_newline(p)

            line = self.file.readline()
            if verbose: print '--', mid, line

            if line < string:
                low = mid + 1
            else:
                high = mid

        p = low
        self._seek_newline(p)

        result = [ ]
        while True:
            line = self.file.readline()
            if not line or not line.startswith(string): break
            if line[-1:] == '\n': line = line[:-1]
            result.append(line)
        return result

    def _seek_newline(self, p):
        while p >= 0:
            self.file.seek(p)
            if self.file.read(1) == '\n': break
            p -= 1
        if p < 0: self.file.seek(0)


# For easy running via a command line one-liner
def main():
    if len(sys.argv) != 3:
        print "Usage: python file_searcher.py filename search_string"
        sys.exit(-1)

    s = Searcher(sys.argv[1])
    results = s.find(sys.argv[2])
    for result in results:
        print result

if __name__ == '__main__':
    main()
