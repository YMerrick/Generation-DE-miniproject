import pytest
from unittest.mock import Mock

mock_file_handler = Mock()

mock_file_handler.load.return_value = [1, 2, 3, 4, 5]


def test_CSVListMenu_add():
    expected = 2

    # result = add(1,1)


def test_CSVListMenu_update():
    pass
