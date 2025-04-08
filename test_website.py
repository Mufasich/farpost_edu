import pytest
from unittest.mock import Mock, patch
from CatFactProcessor import CatFactProcessor, APIError

def test_class_init():
    web = CatFactProcessor()
    assert web.last_content == ""

# тест при запросе
def test_get_content_failure():
    with patch('requests.get', side_effect=Exception("Connection failed")):
        processor = CatFactProcessor()

        with pytest.raises(APIError, match="Ошибка при запросе к API"):
            processor.get_content("https://404.com")