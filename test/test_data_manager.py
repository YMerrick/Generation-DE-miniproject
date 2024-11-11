import pytest

from src import DataManagerInterface, DictDataManager

@pytest.fixture(scope='module')
def string_stub_data():
    return ['test', 'untest']

@pytest.fixture(scope='module')
def dict_stub_data():
    return [
        {'header1': 'test',
         'header2': 'untest'},
        {'header1': 'another',
         'header2': 'new'},
        {'header1': 'analogy',
         'header2': 'synonym'},
        ]

@pytest.fixture(scope='module')
def dict_data_manager(dict_stub_data):
    return DictDataManager(dict_stub_data)

def test_DataManagerInterface():
    class TestClass(DataManagerInterface):
        def __init__(self):
            super().__init__()

        def add(self):
            return super().add()
        
        def update(self):
            return super().update()
        
        def delete_element(self):
            return super().delete_element()
        
    result = TestClass()

    with pytest.raises(NotImplementedError):
        result.add()

    with pytest.raises(NotImplementedError):
        result.update()

    with pytest.raises(NotImplementedError):
        result.delete_element()

def test_string_add(str_data_manager, string_stub_data):
    expected = string_stub_data + ['another']
    assert expected == str_data_manager.add('another')

def test_string_update(str_data_manager):
    expected = 'new'
    index = 3
    assert expected == str_data_manager.update(index, 'new')

def test_string_delete(str_data_manager):
    expected = 'new'
    index = 3
    assert expected == str_data_manager.delete_element(index)

def test_string_get_data(str_data_manager, string_stub_data):
    expected = string_stub_data
    assert expected == str_data_manager.get_data()

def test_select_columns_fail(dict_data_manager):
    assert dict_data_manager.select_columns('headers') is None

def test_select_columns(dict_data_manager):
    expected = [
        {'header2': 'untest'},
        {'header2': 'new'},
        {'header2': 'synonym'}
    ]
    assert expected == dict_data_manager.select_columns('header2')

def test_filter_on_column_fail(dict_data_manager):
    assert dict_data_manager.filter_on_column('headers', 'hello') is None

def test_filter_on_column(dict_data_manager):
    expected = [{'header1': 'another', 'header2': 'new'}]
    assert expected == dict_data_manager.filter_on_column('header1', 'another')

def test_dict_add(dict_data_manager, dict_stub_data):
    expected = dict_stub_data + [{'header1' : 'nice', 'header2': 'coupling'}]
    dict_data_manager.add({'header1' : 'nice', 'header2': 'coupling'})
    assert expected == dict_data_manager.user_list

def test_dict_update(dict_data_manager):
    index = 4
    property_selection = 'header2'
    new_property = 'better'
    expected = {'header1' : 'nice', 'header2': 'better'}

    assert expected == dict_data_manager.update(index, property_selection, new_property)

def test_dict_delete(dict_data_manager):
    index = 4
    expected = {'header1' : 'nice', 'header2': 'better'}
    assert expected == dict_data_manager.delete_element(index)

def test_get_keys(dict_data_manager):
    expected = ['header1', 'header2']
    assert expected == dict_data_manager.get_keys()

def test_get_data(dict_data_manager, dict_stub_data):
    assert dict_stub_data == dict_data_manager.get_data()

def test_get_length(dict_data_manager):
    expected = 3
    assert expected == dict_data_manager.get_length()