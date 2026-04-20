import pytest
import os
import json
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from pageindex.core.logging import JsonLogger

@pytest.fixture
def mock_datetime():
    with patch('pageindex.core.logging.datetime') as mock_date:
        fixed_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_date.now.return_value = fixed_now
        mock_date.isoformat.return_value = fixed_now.isoformat()
        yield mock_date

@pytest.fixture
def mock_pdf_name():
    with patch('pageindex.core.logging.get_pdf_name') as mock_get:
        mock_get.return_value = "test_pdf"
        yield mock_get

@pytest.fixture
def mock_os_makedirs():
    with patch('os.makedirs') as mock_make:
        yield mock_make

def test_json_logger_init(mock_os_makedirs, mock_pdf_name, mock_datetime):
    logger = JsonLogger("some_path.pdf")

    assert logger.filename == "test_pdf_20230101_120000.json"
    mock_os_makedirs.assert_called_once_with("./logs", exist_ok=True)
    assert logger.log_data == []

def test_json_logger_log_string(mock_os_makedirs, mock_pdf_name, mock_datetime):
    m = mock_open()
    with patch('builtins.open', m):
        logger = JsonLogger("some_path.pdf")
        logger.log("INFO", "test message")

        assert len(logger.log_data) == 1
        entry = logger.log_data[0]
        assert entry['level'] == "INFO"
        assert entry['message'] == "test message"
        assert 'timestamp' in entry

        m.assert_called_once_with(os.path.join("logs", logger.filename), "w", encoding='utf-8')

        # Verify json.dump was called (it's called via open)
        # We can also check what was written
        handle = m()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        parsed_content = json.loads(written_content)
        assert parsed_content == logger.log_data

def test_json_logger_log_dict(mock_os_makedirs, mock_pdf_name, mock_datetime):
    m = mock_open()
    with patch('builtins.open', m):
        logger = JsonLogger("some_path.pdf")
        message_dict = {"msg": "detailed message", "code": 123}
        logger.log("ERROR", message_dict, extra="data")

        assert len(logger.log_data) == 1
        entry = logger.log_data[0]
        assert entry['level'] == "ERROR"
        assert entry['msg'] == "detailed message"
        assert entry['code'] == 123
        assert entry['extra'] == "data"

def test_json_logger_convenience_methods(mock_os_makedirs, mock_pdf_name, mock_datetime):
    m = mock_open()
    with patch('builtins.open', m):
        logger = JsonLogger("some_path.pdf")

        logger.info("info msg")
        assert logger.log_data[-1]['level'] == "INFO"

        logger.error("error msg")
        assert logger.log_data[-1]['level'] == "ERROR"

        logger.debug("debug msg")
        assert logger.log_data[-1]['level'] == "DEBUG"

        logger.exception("exception msg")
        assert logger.log_data[-1]['level'] == "ERROR"
        assert logger.log_data[-1]['exception'] is True

def test_json_logger_filepath(mock_os_makedirs, mock_pdf_name, mock_datetime):
    logger = JsonLogger("some_path.pdf")
    expected_path = os.path.join("logs", logger.filename)
    assert logger._filepath() == expected_path
