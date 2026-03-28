import sys
from unittest.mock import MagicMock

# Mock all potential problematic modules
mock_modules = [
    'tiktoken', 'openai', 'dotenv', 'fitz', 'pdfplumber', 'loguru', 'PyPDF2', 'pymupdf'
]
for module in mock_modules:
    sys.modules[module] = MagicMock()

# Mock internal submodules to avoid relative import errors when running tests as a package
sys.modules['pageindex.core.llm'] = MagicMock()
sys.modules['pageindex.core.pdf'] = MagicMock()
