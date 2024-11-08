import pytest
from unittest.mock import Mock
from io import StringIO

from app import save, save_all, main_menu_choice, main, print_main_menu

@pytest.fixture(scope='module')
def data_manager():
    manager = Mock()
    manager.get_data.return_value = ['This is a stub list']
    return manager

@pytest.fixture(scope='module')
def handler():
    file_handler = Mock()
    file_handler.save.return_value = True
    return file_handler

@pytest.fixture(scope='module')
def handler_list(handler):
    list_of_handler = [handler]
    return list_of_handler

@pytest.fixture(scope='module')
def data_list(data_manager):
    list_of_data = [data_manager]
    return list_of_data

def test_save(handler, data_manager):
    assert save(handler, data_manager)
    data_manager.get_data.assert_called()
    handler.save.assert_called_once_with(data_manager.get_data())
    handler.reset_mock()
    data_manager.reset_mock()

def test_save_all(handler_list, data_list, handler, data_manager):
    assert save_all(handler_list, data_list)
    data_manager.get_data.assert_called()
    handler.save.assert_called_once_with(data_manager.get_data())
    handler.reset_mock()
    data_manager.reset_mock()

def test_print_main_menu(capsys):
    output = "1. Products Menu\n2. Courier Menu\n3. Orders Menu\n0. Exit\n"
    print_main_menu()
    captured = capsys.readouterr()
    assert captured.out == output

def test_main_menu_choice():
    assert False

def test_main():
    assert False
