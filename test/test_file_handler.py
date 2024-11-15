import os
from io import TextIOWrapper

import pytest

from src import CSVFile
from src.file_handler import DataHandler


@pytest.fixture
def stub_data():
    return [
        {'test': 'test',
         'untest': 'untest'},
        {'test': 'function',
         'untest': 'another'}
        ]


@pytest.fixture(scope='module')
def test_file():
    return "test_file.csv"


@pytest.fixture(scope='module')
def file_handler(test_file):
    handler = CSVFile(test_file)

    # Cleaning up the file before each test
    yield handler

    # Clean up after the test
    if os.path.exists(test_file):
        os.remove(test_file)


def test_fail_open_file_pass_none():
    with pytest.raises(Exception):
        CSVFile(None).open_file(mode='rt')


def test_open_file_file_not_found(file_handler, test_file):
    expected = file_handler.open_file()
    assert os.path.exists(test_file)
    assert isinstance(expected, TextIOWrapper)


def test_open_file(file_handler, test_file):
    expected = file_handler.open_file()

    assert os.path.exists(test_file)
    assert isinstance(expected, TextIOWrapper)
    assert not expected.closed


def test_save_falsy(file_handler):
    data = []
    expected = file_handler.save(data)
    assert not expected


def test_save_headers(file_handler, stub_data, test_file):
    file_handler.save(stub_data)
    expected = ['test', 'untest']

    result: list
    with open(test_file) as file:
        result = [header.rstrip() for header in file.readline().split(',')]

    assert expected == result


def test_save_headers_template(file_handler, stub_data, test_file):
    file_handler.save(stub_data, template={'test': None, 'untest': None})
    expected = ['test', 'untest']

    result: list
    with open(test_file) as file:
        result = [header.rstrip() for header in file.readline().split(',')]

    assert expected == result


def test_save_truty(file_handler, stub_data):
    expected = file_handler.save(stub_data)
    assert expected


def test_load(file_handler):
    result_list = file_handler.load()
    assert len(result_list) > 0
    assert isinstance(result_list, list)
    assert isinstance(result_list[0], dict)


def test_get_headers(file_handler):
    expected = ['test', 'untest']
    result_headers = file_handler.get_headers()
    assert isinstance(result_headers, list)
    assert expected == result_headers


def test_DataHandler():
    class TestClass(DataHandler):
        def __init__(self):
            super().__init__()

        def load(self):
            super().load()

        def save(self):
            super().save()

    result = TestClass()

    with pytest.raises(NotImplementedError):
        result.save()

    with pytest.raises(NotImplementedError):
        result.load()
