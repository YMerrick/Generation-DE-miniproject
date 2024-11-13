import pytest
from unittest.mock import Mock
from io import StringIO

from src.app import save, save_all, main_menu_choice, menu, print_main_menu


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


@pytest.fixture(scope='module')
def stub_menu():
    mock_menu = Mock()
    mock_menu.start.return_value = None
    return mock_menu


@pytest.fixture(scope='module')
def stub_menu_list(stub_menu):
    mock_menu_list = [stub_menu]
    return mock_menu_list


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


def test_main_menu_choice(monkeypatch, stub_menu_list,
                          handler_list, data_list, stub_menu):
    monkeypatch.setattr('sys.stdin', StringIO('1\n'))
    expected = True

    result = main_menu_choice(stub_menu_list, handler_list, data_list)

    assert expected == result
    stub_menu.start.assert_called()

    stub_menu.reset_mock()
    handler_list[0].reset_mock()
    data_list[0].reset_mock()


def test_main_menu_choice_invalid_input(monkeypatch, capsys,
                                        stub_menu_list, handler_list,
                                        data_list):
    monkeypatch.setattr('sys.stdin', StringIO('10\n'))

    expected = 'Please select a valid option\n'
    main_menu_choice(stub_menu_list, handler_list, data_list)
    captured = capsys.readouterr().out

    assert expected in captured

    stub_menu_list[0].reset_mock()
    handler_list[0].reset_mock()
    data_list[0].reset_mock()


def test_main_menu_choice_exit(monkeypatch, stub_menu_list,
                               handler_list, data_list):
    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    expected = False

    assert expected == main_menu_choice(stub_menu_list,
                                        handler_list,
                                        data_list)
    handler_list[0].save.assert_called()
    data_list[0].get_data.assert_called()

    stub_menu_list[0].reset_mock()
    handler_list[0].reset_mock()
    data_list[0].reset_mock()


def test_menu(monkeypatch, stub_menu_list, handler_list, data_list):
    monkeypatch.setattr('sys.stdin', StringIO('1\n'))
    expected = True

    assert expected == menu(stub_menu_list, handler_list, data_list)

    stub_menu_list[0].reset_mock()
    handler_list[0].reset_mock()
    data_list[0].reset_mock()
