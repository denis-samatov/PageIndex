import sys
from unittest.mock import MagicMock

# Mock all potential problematic modules
mock_modules = [
    'tiktoken', 'openai', 'dotenv', 'fitz', 'pdfplumber', 'loguru', 'PyPDF2', 'pymupdf'
]
for module in mock_modules:
    sys.modules[module] = MagicMock()

# Setup tiktoken mock to behave more realistically for test_count_tokens
mock_tiktoken = sys.modules['tiktoken']
mock_encoding = MagicMock()
mock_encoding.encode.return_value = [1, 2, 3] # Dummy tokens
mock_tiktoken.encoding_for_model.return_value = mock_encoding
mock_tiktoken.get_encoding.return_value = mock_encoding
