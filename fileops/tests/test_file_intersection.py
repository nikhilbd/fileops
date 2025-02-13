import unittest
import os
import tempfile
from fileops.file_intersection import process_file_intersection


class TestFileIntersection(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create left file
        self.left_file = os.path.join(self.test_dir, 'left.csv')
        with open(self.left_file, 'w', encoding='utf-8') as f:
            f.write('1,A,X\n')
            f.write('2,B,Y\n')
            f.write('3,C,Z\n')
            f.write('4,D,W\n')
        
        # Create right file
        self.right_file = os.path.join(self.test_dir, 'right.csv')
        with open(self.right_file, 'w', encoding='utf-8') as f:
            f.write('1,A,X,Extra1\n')
            f.write('3,C,Z,Extra2\n')
    
    def tearDown(self):
        # Clean up temporary files
        os.unlink(self.left_file)
        os.unlink(self.right_file)
        os.rmdir(self.test_dir)

    def test_basic_intersection(self):
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_columns='0',
            right_columns='0',
            left_delim=',',
            right_delim=','
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ['1', 'A', 'X'])
        self.assertEqual(result[1], ['3', 'C', 'Z'])

    def test_multiple_columns(self):
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_columns='0,1',
            right_columns='0,1',
            left_delim=',',
            right_delim=','
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ['1', 'A', 'X'])
        self.assertEqual(result[1], ['3', 'C', 'Z'])

    def test_insert_columns(self):
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_columns='0',
            right_columns='0',
            left_delim=',',
            right_delim=',',
            insert_cols='3'
        )
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ['1', 'A', 'X', 'Extra1'])
        self.assertEqual(result[1], ['3', 'C', 'Z', 'Extra2'])

    def test_case_sensitive(self):
        # Create files with mixed case
        with open(self.left_file, 'w', encoding='utf-8') as f:
            f.write('1,A,X\n')
            f.write('2,b,Y\n')
        
        with open(self.right_file, 'w', encoding='utf-8') as f:
            f.write('1,A,X\n')
            f.write('2,B,Y\n')
        
        # Test case-sensitive (should not find match for row 2)
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_columns='1',
            right_columns='1',
            left_delim=',',
            right_delim=','
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ['1', 'A', 'X'])
        
        # Test case-insensitive (should find both matches)
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_columns='1',
            right_columns='1',
            left_delim=',',
            right_delim=',',
            lower_case=True
        )
        self.assertEqual(len(result), 2)

    def test_empty_files(self):
        # Create empty files
        with open(self.left_file, 'w', encoding='utf-8') as f:
            pass
        with open(self.right_file, 'w', encoding='utf-8') as f:
            pass
        
        result = process_file_intersection(
            self.left_file,
            self.right_file,
            left_delim=',',
            right_delim=','
        )
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main() 