import unittest
from unittest.mock import MagicMock
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Mock dependencies
for module in ['tiktoken', 'openai', 'dotenv', 'fitz', 'pdfplumber', 'loguru', 'PyPDF2', 'pymupdf']:
    sys.modules[module] = MagicMock()

# Mock relative imports by providing the modules in sys.modules
# For tree.py, it does 'from .llm import ...' and 'from .pdf import ...'
# When running tree.py, its __name__ will be 'pageindex.core.tree' (if imported normally)
# or just 'tree' if loaded via importlib.
# Let's try to make it work for both.
sys.modules['pageindex.core.llm'] = MagicMock()
sys.modules['pageindex.core.pdf'] = MagicMock()
sys.modules['.llm'] = MagicMock()
sys.modules['.pdf'] = MagicMock()

from pageindex.core.tree import convert_physical_index_to_int

class TestConvertPhysicalIndex(unittest.TestCase):
    def test_string_conversion_bracketed(self):
        self.assertEqual(convert_physical_index_to_int("<physical_index_5>"), 5)
        self.assertEqual(convert_physical_index_to_int("<physical_index_00123>"), 123)

    def test_string_conversion_plain(self):
        self.assertEqual(convert_physical_index_to_int("physical_index_5"), 5)
        self.assertEqual(convert_physical_index_to_int("physical_index_789"), 789)

    def test_list_conversion(self):
        data = [
            {"title": "A", "physical_index": "<physical_index_1>"},
            {"title": "B", "physical_index": "physical_index_2"},
            {"title": "C", "physical_index": 3}
        ]
        convert_physical_index_to_int(data)
        self.assertEqual(data[0]["physical_index"], 1)
        self.assertEqual(data[1]["physical_index"], 2)
        self.assertEqual(data[2]["physical_index"], 3)

    def test_nested_structure(self):
        data = [
            {
                "title": "Chapter 1",
                "physical_index": "<physical_index_1>",
                "nodes": [
                    {"title": "Section 1.1", "physical_index": "<physical_index_2>"}
                ]
            }
        ]
        convert_physical_index_to_int(data)
        self.assertEqual(data[0]["physical_index"], 1)
        self.assertEqual(data[0]["nodes"][0]["physical_index"], 2)

    def test_dict_input(self):
        data = {"title": "A", "physical_index": "<physical_index_10>"}
        result = convert_physical_index_to_int(data)
        self.assertEqual(result["physical_index"], 10)

    def test_deeply_nested_dict(self):
        data = {
            "a": {
                "b": {
                    "physical_index": "physical_index_42"
                }
            }
        }
        convert_physical_index_to_int(data)
        self.assertEqual(data["a"]["b"]["physical_index"], 42)

    def test_invalid_formats(self):
        self.assertEqual(convert_physical_index_to_int("something_else"), "something_else")
        self.assertEqual(convert_physical_index_to_int("<not_index_5>"), "<not_index_5>")
        self.assertEqual(convert_physical_index_to_int(123), 123)

    def test_edge_cases(self):
        self.assertEqual(convert_physical_index_to_int([]), [])
        self.assertEqual(convert_physical_index_to_int({}), {})
        self.assertIsNone(convert_physical_index_to_int(None))

if __name__ == "__main__":
    unittest.main()
