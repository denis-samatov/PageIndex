import unittest
from unittest.mock import MagicMock
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Mock dependencies
for module in ['tiktoken', 'openai', 'dotenv', 'fitz', 'pdfplumber', 'loguru', 'PyPDF2', 'pymupdf']:
    sys.modules[module] = MagicMock()

# Mock relative imports
sys.modules['pageindex.core.llm'] = MagicMock()
sys.modules['pageindex.core.pdf'] = MagicMock()
sys.modules['.llm'] = MagicMock()
sys.modules['.pdf'] = MagicMock()

from pageindex.core.tree import list_to_tree, structure_to_list, write_node_id

class TestTree(unittest.TestCase):
    def setUp(self):
        self.sample_structure = [
            {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 5},
            {"structure": "1.1", "title": "Section 1.1", "start_index": 1, "end_index": 3},
            {"structure": "1.2", "title": "Section 1.2", "start_index": 4, "end_index": 5},
            {"structure": "2", "title": "Chapter 2", "start_index": 6, "end_index": 10}
        ]

    def test_list_to_tree(self):
        sample_structure = self.sample_structure
        tree = list_to_tree(sample_structure)
        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0]["title"], "Chapter 1")
        self.assertEqual(len(tree[0]["nodes"]), 2)
        self.assertEqual(tree[0]["nodes"][0]["title"], "Section 1.1")
        self.assertEqual(tree[1]["title"], "Chapter 2")
        self.assertTrue("nodes" not in tree[1] or len(tree[1]["nodes"]) == 0)

    def test_structure_to_list(self):
        sample_structure = self.sample_structure
        tree = list_to_tree(sample_structure)
        flat_list = structure_to_list(tree)
        self.assertEqual(len(flat_list), 4)
        titles = [item["title"] for item in flat_list]
        self.assertIn("Chapter 1", titles)
        self.assertIn("Section 1.1", titles)

    def test_write_node_id(self):
        sample_structure = self.sample_structure
        tree = list_to_tree(sample_structure)
        write_node_id(tree)
        self.assertEqual(tree[0]["node_id"], "0000")
        self.assertEqual(tree[0]["nodes"][0]["node_id"], "0001")

if __name__ == "__main__":
    unittest.main()
