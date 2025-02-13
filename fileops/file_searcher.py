#!/usr/bin/python3
"""Binary search within a sorted file for lines starting with a given string.

This module provides a Searcher class that performs binary search within a sorted text file
to find lines that start with a given string. It assumes the file is in UTF-8 encoding
and the lines are sorted.

Example:
    searcher = Searcher('file_path')
    results = searcher.find('test string')
"""

import sys
from typing import List, Optional, Tuple


class Searcher:
    """Binary search for lines starting with a given string in a sorted file."""

    def __init__(self, file_path: str) -> None:
        """Initialize with the path to the file to search."""
        self.file_path = file_path
        self.file = None

    def __enter__(self) -> 'Searcher':
        """Context manager entry."""
        self.file = open(self.file_path, 'r', encoding='utf-8', errors='replace')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def _read_line_at_pos(self, pos: int) -> Tuple[int, str]:
        """Read a complete line starting at or after the given position.
        
        Args:
            pos: Position to start reading from

        Returns:
            Tuple of (start position of line, line without newline)
        """
        self.file.seek(pos)

        # If we're not at the start of the file, read until next newline
        if pos > 0:
            self.file.readline()

        # Get position of complete line
        line_pos = self.file.tell()
        line = self.file.readline().rstrip('\n')

        return line_pos, line

    def _compare_strings(self, a: str, b: str) -> int:
        """Compare two strings, handling Unicode correctly.
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            -1 if a < b, 0 if a == b, 1 if a > b
        """
        if a.startswith(b):
            return 0
        return -1 if a < b else 1

    def _find_first_match(self, search_string: str, verbose: bool) -> Optional[int]:
        """Binary search to find the first matching line.
        
        Args:
            search_string: String to search for
            verbose: Whether to print debug information
            
        Returns:
            Position of first match, or None if no match found
        """
        self.file.seek(0, 2)  # Seek to end
        file_size = self.file.tell()

        if file_size == 0:
            return None

        left = 0
        right = file_size
        match_pos = None

        while left < right:
            mid = (left + right) // 2
            pos, line = self._read_line_at_pos(mid)

            if verbose:
                print(f"Searching at position {mid}, found line: {line}")

            if not line:  # Handle EOF
                right = mid
                continue

            cmp_result = self._compare_strings(line, search_string)

            if cmp_result == 0:  # Match found
                # Found a match, but need to check if there are matches before this
                match_pos = pos

                # Try to read the previous line
                if pos > 0:
                    self.file.seek(pos - 1)
                    self.file.readline()  # Read and discard partial line
                    prev_line = self.file.readline().rstrip('\n')

                    if prev_line.startswith(search_string):
                        # There might be matches before this one
                        right = mid
                        continue

                # No matches before this one, we can stop
                return match_pos

            if cmp_result < 0:  # Line is less than search string
                left = pos + len(line.encode('utf-8')) + 1  # Skip current line
            else:  # Line is greater than search string
                right = mid

        # If we found a match during the search, return it
        return match_pos

    def find(self, search_string: str, verbose: bool = False) -> List[str]:
        """Find all lines that start with the given string using binary search.
        
        Args:
            search_string: String to search for at the start of lines
            verbose: Whether to print debug information
            
        Returns:
            List of matching lines
        """
        matches = []

        # Find first match using binary search
        first_match_pos = self._find_first_match(search_string, verbose)

        if first_match_pos is None:
            return matches

        # Scan forward to collect all matches
        self.file.seek(first_match_pos)
        while True:
            line = self.file.readline().rstrip('\n')
            if not line:
                break

            if line.startswith(search_string):
                matches.append(line)
            elif self._compare_strings(line, search_string) > 0:
                break  # Stop if we've passed possible matches

        return matches

    def close(self) -> None:
        """Close the file."""
        if self.file:
            self.file.close()
            self.file = None

    def __del__(self) -> None:
        """Ensure the file is closed when the object is destroyed."""
        self.close()


def main() -> None:
    """Command-line interface for the file searcher."""
    if len(sys.argv) != 3:
        print('Usage: python file_searcher.py filename search_string')
        sys.exit(-1)

    with Searcher(sys.argv[1]) as searcher:
        results = searcher.find(sys.argv[2])
        for result in results:
            print(result)


if __name__ == '__main__':
    main()
