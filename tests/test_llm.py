import pytest
from pageindex.core.llm import extract_json, count_tokens

def test_extract_json_basic():
    text = '{"key": "value"}'
    assert extract_json(text) == {"key": "value"}

def test_extract_json_with_markdown():
    text = 'Here is the json:\n```json\n{"key": "value"}\n```'
    assert extract_json(text) == {"key": "value"}

def test_extract_json_with_trailing_commas():
    # Simple trailing comma in object
    text = '{"key": "value",}'
    assert extract_json(text) == {"key": "value"}

    # Trailing comma with whitespace in object
    text = '{"key": "value" , }'
    assert extract_json(text) == {"key": "value"}

    # Trailing comma in array
    text = '[1, 2, 3,]'
    assert extract_json(text) == [1, 2, 3]

    # Trailing comma with whitespace in array
    text = '[1, 2, 3 , ]'
    assert extract_json(text) == [1, 2, 3]

def test_extract_json_nested_trailing_commas():
    text = '{"a": [1, ], "b": {"c": 2, }}'
    assert extract_json(text) == {"a": [1], "b": {"c": 2}}

def test_count_tokens():
    text = "Hello world"
    # Basic check, exact number depends on encoding
    assert count_tokens(text) > 0
