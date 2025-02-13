#!/usr/bin/python3
# Copyright 2013 Foursquare Labs Inc. All Rights Reserved.
#
# For unicode csv reader & writer support
# See https://docs.python.org/3/library/csv.html for more info

import csv
import codecs
import io
from typing import Iterator, List, TextIO, Any


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f: TextIO, encoding: str) -> None:
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self) -> 'UTF8Recoder':
        return self

    def __next__(self) -> str:
        return self.reader.__next__()


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f: TextIO, dialect: csv.Dialect = csv.excel, encoding: str = "utf-8", **kwds: Any) -> None:
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def __next__(self) -> List[str]:
        row = next(self.reader)
        return [str(s) for s in row]

    def __iter__(self) -> 'UnicodeReader':
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f: TextIO, dialect: csv.Dialect = csv.excel, encoding: str = "utf-8", **kwds: Any) -> None:
        self.queue = io.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row: List[str]) -> None:
        self.writer.writerow(row)
        data = self.queue.getvalue()
        self.stream.write(data)
        self.queue.truncate(0)
        self.queue.seek(0)

    def writerows(self, rows: Iterator[List[str]]) -> None:
        for row in rows:
            self.writerow(row)
