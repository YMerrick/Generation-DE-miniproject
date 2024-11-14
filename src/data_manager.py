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
from typing import Iterable

from tabulate import tabulate
from psycopg2.extensions import cursor
from psycopg2.sql import SQL, Identifier, Literal, Placeholder

from .compse_db_query import Composer


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
    def __init__(self, cur: cursor, table_name: str):
        super().__init__()
        self.cur = cur
        self.table_name = table_name
        self.columns = self.__get_columns()

    def __del__(self):
        self.cur.close()

    def __get_columns(self):
        query = Composer('select')
        query.add_field(
            Identifier('column_name')
            ).add_from(
                Identifier('information_schema', 'columns')
                ).where(
                    Composer.eq_stmt(
                        Identifier('table_name'),
                        Literal(self.table_name)
                        )
                    )
        self.cur.execute(query.get_query())
        return [header[0] for header in self.cur.fetchall()]

    def verify_columns(self, columns):
        return any((column not in self.columns for column in columns))

    def convert_fetch(self, fetched: Iterable,
                      columns: list[str]) -> list[dict]:
        return [{c: v for c, v in zip(columns, row)} for row in fetched]

    def add(self, values: list, columns: list[str] | None = None):
        '''Adds an entry into a table'''
        if not columns:
            columns = self.columns
        else:
            if self.verify_columns(columns):
                raise ValueError('Column does not exist')
        sql = Composer('insert').into(self.table_name)
        if len(columns) < len(self.columns):
            column_field = Composer.make_fields(
                *(Identifier(column) for column in columns)
                )
            column_field = SQL('({})').format(column_field)
            sql.add_field(column_field)
        value_field = Composer.make_fields(
            *(Literal(value) for value in values)
            )
        value_field = SQL('({})').format(value_field)
        sql.values(value_field)
        sql.returning(column_field)
        self.cur.execute(sql.get_query())
        return self.convert_fetch(self.cur.fetchall(), self.columns)

    def update(self, values: dict, condition: dict):
        '''Updates an entry in a table'''
        if self.verify_columns(values.keys()):
            raise ValueError('column does not exist')
        if self.verify_columns(condition.keys()):
            raise ValueError('column does not exist')
        sql = Composer('update').add_field(Identifier(self.table_name))
        values_gen = (Composer.eq_stmt(
            Identifier(k), Literal(v)) for k, v in values.items())
        values_field = Composer.make_fields(*values_gen)
        sql._set(values_field)
        condition_gen = Composer.make_fields(
            *(Composer.eq_stmt(
                Identifier(k), Literal(v)) for k, v in condition.items())
            )
        sql.where(condition_gen)
        columns = Composer.make_fields(
            *(Identifier(column) for column in self.columns)
        )
        sql.returning(columns)
        self.cur.execute(sql.get_query())
        return self.convert_fetch(self.cur.fetchall(), self.columns)

    def delete_element(self, column, value):
        '''Deletes an entry in a table'''
        sql = Composer('delete').add_from(Identifier(self.table_name))
        condition = Composer.eq_stmt(Identifier(column), Placeholder())
        sql.where(condition)
        sql.returning(
            Composer.make_fields(
                *(Identifier(column) for column in self.columns)
                )
            )
        self.cur.execute(sql, value)
        return self.convert_fetch(self.cur.fetchall(), self.columns)

    def get(self, columns: list[str] | None = None):
        '''Retrieves entry in a table'''
        if not columns:
            columns = self.columns
        else:
            if self.verify_columns(columns):
                raise ValueError('Column does not exist')

        sql = Composer('select')
        fields = Composer.make_fields(
            *(Identifier(column) for column in columns)
            )
        sql.add_field(fields).add_from(Identifier(self.table_name))
        self.cur.execute(sql.get_query())
        return self.convert_fetch(self.cur.fetchall(), columns)

    def check_exists(self, condition: dict) -> bool:
        '''Checks if an entry exists in a table'''
        sql = Composer('select').add_field(Literal(1))
        sql.add_from(Identifier(self.table_name))
        clause = Composer.make_fields(
            *(Composer.eq_stmt(
                Identifier(k), Literal(v)) for k, v in condition.items())
            )
        sql.where(clause)
        self.cur.execute(sql.get_query())
        return True if self.cur.fetchall() else False


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
