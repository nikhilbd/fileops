import unittest
import os
import tempfile
import shutil
from fileops.file_select_ops import process_select_operations

class TestFileSelectOps(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
        # CSV Test File with Unicode
        self.test_file_csv = os.path.join(self.test_dir, 'sample.csv')
        with open(self.test_file_csv, 'w', encoding='utf-8') as f:
            f.write("name,category,value,city\n")
            f.write("item1,A,10,New York\n")
            f.write("itemČ,B,20,London\n")
            f.write("item1,A,5,Paris\n")
            f.write("itemÖ,C,30,Berlin\n")
            f.write("itemČ,B,15,London\n")
            f.write("itemØ,A,25,New York\n")

        # TSV Test File with Unicode
        self.test_file_tsv = os.path.join(self.test_dir, 'sample.tsv')
        with open(self.test_file_tsv, 'w', encoding='utf-8') as f:
            f.write("name\tcategory\tvalue\tcity\n")
            f.write("item1\tA\t10\tNew York\n")
            f.write("itemČ\tB\t20\tLondon\n")
            f.write("item1\tA\t5\tParis\n")
            f.write("itemÖ\tC\t30\tBerlin\n")
            f.write("itemČ\tB\t15\tLondon\n")
            f.write("itemØ\tA\t25\tNew York\n")

        # Empty file
        self.empty_file = os.path.join(self.test_dir, 'empty.txt')
        open(self.empty_file, 'w').close()

        # File with only header
        self.header_only_file_csv = os.path.join(self.test_dir, 'header_only.csv')
        with open(self.header_only_file_csv, 'w', encoding='utf-8') as f:
            f.write("name,category,value,city\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_simple_sum_aggregation(self):
        # Select category (col 1), sum value (col 2)
        # Expected output: [['A', '15.0'], ['B', '35.0'], ['C', '30.0']] (order might vary) for original sample
        # Updated for new self.test_file_csv:
        # A: 10 (item1) + 5 (item1) + 25 (itemØ) = 40
        # B: 20 (itemČ) + 15 (itemČ) = 35
        # C: 30 (itemÖ) = 30
        # Expected: [['A', '40.0'], ['B', '35.0'], ['C', '30.0']]
        
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='1',  # category
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char=','
        )
        
        expected_result = [['A', '40.0'], ['B', '35.0'], ['C', '30.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_sum_aggregation_with_where_clause(self):
        # Select category (col 1), sum value (col 2)
        # WHERE category (col 1) != 'A'
        # Using self.test_file_csv:
        # B: 20 (itemČ) + 15 (itemČ) = 35
        # C: 30 (itemÖ) = 30
        # Expected output: [['B', '35.0'], ['C', '30.0']]
        
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='1',  # category
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=['1!=A'], # category != 'A'
            delimiter_char=','
        )
        
        expected_result = [['B', '35.0'], ['C', '30.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_count_aggregation(self):
        # Select category (col 1), count occurrences (col 1)
        # Using self.test_file_csv:
        # A: item1, item1, itemØ (3)
        # B: itemČ, itemČ (2)
        # C: itemÖ (1)
        # Expected output: [['A', '3'], ['B', '2'], ['C', '1']] (order might vary)
        
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='1',  # category
            aggregate_cols_str='1',  # category (for count)
            agg_function='count',
            where_clauses_list=None,
            delimiter_char=','
        )
        
        expected_result = [['A', '3'], ['B', '2'], ['C', '1']]
        self.assertEqual(sorted(result), sorted(expected_result))
        
    def test_multiple_select_cols_sum_aggregation(self):
        # Select name (col 0) and category (col 1), sum value (col 2)
        # Using self.test_file_csv:
        # item1,A -> 10 + 5 = 15
        # itemČ,B -> 20 + 15 = 35
        # itemÖ,C -> 30
        # itemØ,A -> 25
        # Expected output: 
        # [['item1', 'A', '15.0'], ['itemČ', 'B', '35.0'], ['itemÖ', 'C', '30.0'], ['itemØ', 'A', '25.0']]
        
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='0,1',  # name, category
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char=','
        )
        
        expected_result = [['item1', 'A', '15.0'], ['itemČ', 'B', '35.0'], ['itemÖ', 'C', '30.0'], ['itemØ', 'A', '25.0']]
        self.assertEqual(sorted(result, key=lambda x: (x[0], x[1])), sorted(expected_result, key=lambda x: (x[0], x[1])))

    def test_sum_aggregation_tab_delimiter(self):
        # Using self.test_file_tsv (same data as csv)
        # Select category (col 1), sum value (col 2)
        # Expected: [['A', '40.0'], ['B', '35.0'], ['C', '30.0']]
        result = process_select_operations(
            input_file_path=self.test_file_tsv,
            select_cols_str='1',  # category
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char='\t'
        )
        expected_result = [['A', '40.0'], ['B', '35.0'], ['C', '30.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_sum_aggregation_unicode_data(self):
        # Using self.test_file_csv
        # Select name (col 0), sum value (col 2)
        # item1 -> 10 + 5 = 15
        # itemČ -> 20 + 15 = 35
        # itemÖ -> 30
        # itemØ -> 25
        # Expected: [['item1', '15.0'], ['itemČ', '35.0'], ['itemÖ', '30.0'], ['itemØ', '25.0']]
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='0',  # name
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char=','
        )
        expected_result = [['item1', '15.0'], ['itemČ', '35.0'], ['itemÖ', '30.0'], ['itemØ', '25.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_sum_aggregation_unicode_where_clause(self):
        # Using self.test_file_csv
        # Select name (col 0), sum value (col 2)
        # WHERE name (col 0) = 'itemČ'
        # itemČ -> 20 + 15 = 35
        # Expected: [['itemČ', '35.0']]
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='0',  # name
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=['0=itemČ'], # name = 'itemČ'
            delimiter_char=','
        )
        expected_result = [['itemČ', '35.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_empty_file(self):
        result = process_select_operations(
            input_file_path=self.empty_file,
            select_cols_str='0',
            aggregate_cols_str='1',
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char=','
        )
        self.assertEqual(result, [])

    def test_file_with_only_header(self):
        result = process_select_operations(
            input_file_path=self.header_only_file_csv,
            select_cols_str='0',
            aggregate_cols_str='1',
            agg_function='sum',
            where_clauses_list=None,
            delimiter_char=','
        )
        self.assertEqual(result, [])

    def test_no_rows_match_where(self):
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='1',  # category
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=['1=X'], # category = 'X' (does not exist)
            delimiter_char=','
        )
        self.assertEqual(result, [])

    def test_complex_where_clause_and_logic(self):
        # Using self.test_file_csv
        # Select name (col 0), sum value (col 2)
        # WHERE category (col 1) = 'A' AND city (col 3) = 'New York'
        # Matches:
        # item1,A,10,New York
        # itemØ,A,25,New York
        # Expected: [['item1', '10.0'], ['itemØ', '25.0']]
        result = process_select_operations(
            input_file_path=self.test_file_csv,
            select_cols_str='0',  # name
            aggregate_cols_str='2',  # value
            agg_function='sum',
            where_clauses_list=['1=A', '3=New York'],
            delimiter_char=','
        )
        expected_result = [['item1', '10.0'], ['itemØ', '25.0']]
        self.assertEqual(sorted(result), sorted(expected_result))

if __name__ == '__main__':
    unittest.main()
