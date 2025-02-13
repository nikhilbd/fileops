import unittest
from fileops.file_ops_common import get_key, split_key, set_ops_parser


class TestFileOpsCommon(unittest.TestCase):
    def test_get_key_single_column(self):
        cols = ["A", "B", "C"]
        key_cols = [0]
        self.assertEqual(get_key(cols, key_cols), "A")

    def test_get_key_multiple_columns(self):
        cols = ["A", "B", "C"]
        key_cols = [0, 2]
        self.assertEqual(get_key(cols, key_cols), "A\tC")

    def test_split_key_single_value(self):
        key = "A"
        self.assertEqual(split_key(key), ["A"])

    def test_split_key_multiple_values(self):
        key = "A\tB\tC"
        self.assertEqual(split_key(key), ["A", "B", "C"])

    def test_set_ops_parser(self):
        parser = set_ops_parser()
        args = parser.parse_args(['left.txt', 'right.txt'])
        
        self.assertEqual(args.left_file, 'left.txt')
        self.assertEqual(args.right_file, 'right.txt')
        self.assertEqual(args.left_columns, '0')
        self.assertEqual(args.right_columns, '0')
        self.assertEqual(args.left_delim, '\t')
        self.assertEqual(args.right_delim, '\t')
        self.assertFalse(args.lower_case)

    def test_set_ops_parser_with_options(self):
        parser = set_ops_parser()
        args = parser.parse_args([
            'left.txt',
            'right.txt',
            '-i',
            '-l', '0,1',
            '-r', '1,2',
            '--left-delim', ',',
            '--right-delim', ';'
        ])
        
        self.assertTrue(args.lower_case)
        self.assertEqual(args.left_columns, '0,1')
        self.assertEqual(args.right_columns, '1,2')
        self.assertEqual(args.left_delim, ',')
        self.assertEqual(args.right_delim, ';')


if __name__ == '__main__':
    unittest.main() 