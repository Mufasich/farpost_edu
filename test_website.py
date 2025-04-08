import pytest
from unittest.mock import Mock, patch
from CatFactProcessor import CatFactProcessor, APIError

def test_class_init():
    processor = CatFactProcessor()
    assert processor.last_fact == ""

# тест при запросе
def test_get_content_failure():
    with patch('requests.get', side_effect=Exception("Connection failed")):
        processor = CatFactProcessor()

        with pytest.raises(APIError, match="Ошибка при запросе к API"):
            processor.get_fact()


def test_empty_analysis():
    processor = CatFactProcessor()
    result = processor.get_fact_analysis()

    assert result == {
        "length": 0,
        "letter_frequencies": {}
    }


def test_get_fact_success():
    mock_response = Mock()
    mock_response.json.return_value = {"fact": "Test fact mock"}
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        processor = CatFactProcessor()
        fact = processor.get_fact()

        assert fact == "Test fact mock"
        assert processor.last_fact == fact