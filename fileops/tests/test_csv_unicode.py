import unittest
import io
from fileops.csv_unicode import UnicodeReader, UnicodeWriter


class TestCSVUnicode(unittest.TestCase):
    def test_unicode_writer(self):
        output = io.StringIO()
        writer = UnicodeWriter(output)
        test_data = [
            ["Hello", "World"],
            ["Café", "Résumé"],
            ["测试", "数据"],
        ]
        writer.writerows(test_data)
        
        # Reset buffer for reading
        output.seek(0)
        content = output.getvalue()
        
        # Verify each row is present
        self.assertIn("Hello,World", content.replace('"', ''))
        self.assertIn("Café,Résumé", content.replace('"', ''))
        self.assertIn("测试,数据", content.replace('"', ''))

    def test_unicode_reader(self):
        input_data = 'Hello,World\nCafé,Résumé\n测试,数据'
        input_file = io.StringIO(input_data)
        reader = UnicodeReader(input_file)
        
        rows = list(reader)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ["Hello", "World"])
        self.assertEqual(rows[1], ["Café", "Résumé"])
        self.assertEqual(rows[2], ["测试", "数据"])

    def test_custom_dialect(self):
        output = io.StringIO()
        writer = UnicodeWriter(output, delimiter=';')
        test_data = [["A", "B"], ["C", "D"]]
        writer.writerows(test_data)
        
        output.seek(0)
        content = output.getvalue()
        self.assertIn("A;B", content)
        self.assertIn("C;D", content)

    def test_empty_rows(self):
        output = io.StringIO()
        writer = UnicodeWriter(output)
        test_data = [[], [""], ["", ""]]
        writer.writerows(test_data)
        
        output.seek(0)
        reader = UnicodeReader(output)
        rows = list(reader)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1], [""])
        self.assertEqual(rows[2], ["", ""])


if __name__ == '__main__':
    unittest.main() 