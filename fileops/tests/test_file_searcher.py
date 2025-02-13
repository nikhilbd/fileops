import unittest
import os
import tempfile
from fileops.file_searcher import Searcher


class TestFileSearcher(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create a sorted test file
        self.test_file = os.path.join(self.test_dir, 'test.txt')
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('apple\n')
            f.write('banana\n')
            f.write('cherry\n')
            f.write('date\n')
            f.write('elderberry\n')
            f.write('fig\n')
    
    def tearDown(self):
        # Clean up temporary files
        os.unlink(self.test_file)
        os.rmdir(self.test_dir)

    def test_basic_search(self):
        with Searcher(self.test_file) as searcher:
            results = searcher.find('cherry', verbose=True)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0], 'cherry')

    def test_prefix_search(self):
        # Create file with multiple matches
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('test1\n')
            f.write('test2\n')
            f.write('test3\n')
            f.write('testing\n')
            f.write('toast\n')
        
        with Searcher(self.test_file) as searcher:
            results = searcher.find('test', verbose=True)
            self.assertEqual(len(results), 4)
            self.assertEqual(results, ['test1', 'test2', 'test3', 'testing'])

    def test_no_match(self):
        with Searcher(self.test_file) as searcher:
            results = searcher.find('zebra', verbose=True)
            self.assertEqual(len(results), 0)

    def test_empty_file(self):
        # Create empty file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            pass
        
        with Searcher(self.test_file) as searcher:
            results = searcher.find('test', verbose=True)
            self.assertEqual(len(results), 0)

    def test_unicode_search(self):
        # Create file with unicode characters
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('caffè\n')            
            f.write('café\n')
            f.write('café au lait\n')
            f.write('coffee\n')
        
        with Searcher(self.test_file) as searcher:
            results = searcher.find('café', verbose=True)
            self.assertEqual(len(results), 2)
            self.assertEqual(results, ['café', 'café au lait'])

if __name__ == '__main__':
    unittest.main() 