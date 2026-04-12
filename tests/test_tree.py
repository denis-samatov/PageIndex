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

from pageindex.core.tree import list_to_tree, structure_to_list, write_node_id, remove_fields

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
        next_id = write_node_id(tree)
        self.assertEqual(tree[0]["node_id"], "0000")
        self.assertEqual(tree[0]["nodes"][0]["node_id"], "0001")
        self.assertEqual(tree[0]["nodes"][1]["node_id"], "0002")
        self.assertEqual(tree[1]["node_id"], "0003")
        self.assertEqual(next_id, 4)

    def test_write_node_id_empty(self):
        self.assertEqual(write_node_id([]), 0)
        self.assertEqual(write_node_id({}), 1) # A single empty dict gets one ID

    def test_write_node_id_flat(self):
        data = [{"title": "A"}, {"title": "B"}]
        next_id = write_node_id(data)
        self.assertEqual(data[0]["node_id"], "0000")
        self.assertEqual(data[1]["node_id"], "0001")
        self.assertEqual(next_id, 2)

    def test_write_node_id_nested(self):
        data = {
            "title": "Root",
            "nodes": [
                {"title": "Child 1", "nodes": [{"title": "Grandchild 1"}]},
                {"title": "Child 2"}
            ]
        }
        next_id = write_node_id(data)
        self.assertEqual(data["node_id"], "0000")
        self.assertEqual(data["nodes"][0]["node_id"], "0001")
        self.assertEqual(data["nodes"][0]["nodes"][0]["node_id"], "0002")
        self.assertEqual(data["nodes"][1]["node_id"], "0003")
        self.assertEqual(next_id, 4)

    def test_write_node_id_custom_start(self):
        data = [{"title": "A"}, {"title": "B"}]
        next_id = write_node_id(data, node_id=10)
        self.assertEqual(data[0]["node_id"], "0010")
        self.assertEqual(data[1]["node_id"], "0011")
        self.assertEqual(next_id, 12)

    def test_write_node_id_multiple_nodes_keys(self):
        # The function checks for 'nodes' in key
        data = {
            "title": "Root",
            "sub_nodes": [{"title": "Sub 1"}],
            "extra_nodes": [{"title": "Extra 1"}]
        }
        next_id = write_node_id(data)
        self.assertEqual(data["node_id"], "0000")
        self.assertEqual(data["sub_nodes"][0]["node_id"], "0001")
        self.assertEqual(data["extra_nodes"][0]["node_id"], "0002")
        self.assertEqual(next_id, 3)

    def test_remove_fields(self):
        # 1. Basic removal of a single field
        data = {"a": 1, "b": 2}
        result = remove_fields(data, fields=["a"])
        self.assertEqual(result, {"b": 2})

        # 2. Removal of multiple fields
        data = {"a": 1, "b": 2, "c": 3}
        result = remove_fields(data, fields=["a", "c"])
        self.assertEqual(result, {"b": 2})

        # 3. Default field removal (defaults to ['text'])
        data = {"title": "Intro", "text": "Some text content"}
        result = remove_fields(data)
        self.assertEqual(result, {"title": "Intro"})

        # 4. Recursive removal from nested dictionaries and lists
        data = {
            "title": "Root",
            "text": "Root text",
            "nodes": [
                {"title": "Child 1", "text": "Child 1 text"},
                {"title": "Child 2", "other": "Keep this"}
            ]
        }
        result = remove_fields(data, fields=["text"])
        expected = {
            "title": "Root",
            "nodes": [
                {"title": "Child 1"},
                {"title": "Child 2", "other": "Keep this"}
            ]
        }
        self.assertEqual(result, expected)

        # 5. Handling of empty structures
        self.assertEqual(remove_fields({}, fields=["a"]), {})
        self.assertEqual(remove_fields([], fields=["a"]), [])

        # 6. Handling of fields not present in the structure
        data = {"a": 1, "b": 2}
        result = remove_fields(data, fields=["c"])
        self.assertEqual(result, data)

        # 7. Ensuring original structure is not modified (immutability)
        data = {"a": 1, "b": {"c": 2, "text": "val"}}
        data_copy = {
            "a": 1,
            "b": {"c": 2, "text": "val"}
        } # Deep copy manually for comparison
        remove_fields(data, fields=["text"])
        self.assertEqual(data, data_copy)

        # 8. Handling of primitive values
        self.assertEqual(remove_fields(123, fields=["a"]), 123)
        self.assertEqual(remove_fields("string", fields=["a"]), "string")

if __name__ == "__main__":
    unittest.main()
