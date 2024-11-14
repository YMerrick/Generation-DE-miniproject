"""File handler class for cheese mongers CLI app.

Class 
Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Usage example:

  foo = CSVFile(filepath)
  bar = foo.load()
  foo.save(data_list, template)
  foobar = foo.get_headers()

TO DO:
    * Finish module doc string
    * 
"""
from abc import ABC, abstractmethod

from tabulate import tabulate
from psycopg2.extensions import connection, cursor


class DataManagerInterface(ABC):

    @abstractmethod
    def add(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_element(self):
        raise NotImplementedError()


class DBDatamanager(DataManagerInterface):
    '''Class used to make and send sql queries to a db connection'''
    def __init__(self, cur: cursor):
        super().__init__()
        self.cur = cur

    def __del__(self):
        self.cur.close()
        super().__del__()

    def add(self):
        '''Adds an entry into a table'''
        return super().add()
    
    def update(self):
        '''Updates an entry in a table'''
        return super().update()
    
    def delete_element(self):
        '''Deletes an entry in a table'''
        return super().delete_element()
    
    def get(self):
        '''Retrieves and entry in a table'''
        pass
    
    def check_exists(self):
        '''Checks if an entry exists in a table'''
        pass


class DictDataManager(DataManagerInterface):

    def __init__(self, input_list: list[dict]):
        super().__init__()
        self.user_list = input_list

    def get_in_tabular_form(self) -> str:
        return tabulate(
            self.user_list,
            headers={
                k: k.replace('_', ' ').capitalize() for k in self.get_keys()
                },
            showindex=(index + 1 for index in range(self.get_length())),
            floatfmt='.2f',
            tablefmt='rounded_grid'
            )

    # Only return selected columns
    def select_columns(self, *cols: list[str]) -> list[dict] | None:
        for col in cols:
            if col not in self.get_keys():
                return None

        new_list = []
        for entry in self.user_list:
            new_list.append({key: entry[key] for key in cols})

        return new_list

    # Return entries matching a search term in specified column
    def filter_on_column(self, col: str,
                         search_term: str) -> list[dict] | None:
        if col not in self.get_keys():
            return None

        return [
            entry for entry in self.user_list
            if search_term.lower() in entry[col].lower()
            ]

    def add(self, new_dict):
        self.user_list.append(new_dict)

    def update(self, user_selection: int,
               property_selected: str,
               updated_property: str) -> dict:
        selected_dict = self.user_list[user_selection - 1]
        selected_dict[property_selected] = updated_property
        return selected_dict

    def delete_element(self, user_selection: int) -> dict:
        return self.user_list.pop(user_selection - 1)

    def get_keys(self) -> list[str] | None:
        if self.user_list:
            return list(self.user_list[0].keys())
        return None

    def get_data(self) -> list[dict]:
        return self.user_list

    def get_length(self) -> int:
        return len(self.user_list)
