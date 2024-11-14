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
    * Finish class doc strings
    * Implement database handler class (This should take the
        queries and run them)
"""
from abc import ABC, abstractmethod
from pathlib import Path
from csv import DictReader, DictWriter
from typing import IO

from psycopg2.extensions import connection, cursor
import psycopg2
from psycopg2.sql import Identifier, Literal

from .compse_db_query import Composer


class DataHandler(ABC):

    @abstractmethod
    def load(self) -> list:
        raise NotImplementedError()

    @abstractmethod
    def save(self) -> bool:
        raise NotImplementedError()


class DBHandler(DataHandler):
    '''Handler for database connections.
    
    Handler class for a database. Establishes a connection and returns cursor
    to be used.
    '''
    def __init__(self, **dsn: dict):
        super().__init__()  
        self.conn: connection = psycopg2.connect(**dsn)

    def load(self) -> cursor:
        cur = self.conn.cursor()
        return cur
    
    def save(self) -> bool:
        self.conn.commit()
        self.conn.close()
        return True
    
    def get_tables(self) -> list:
        # Gets all the tables
        query = Composer('select')
        query.dml = Composer.my_format('', query.dml, Identifier('table_name'))

        where_clause = Composer.eq_stmt(Identifier('table_schema'),
                                        Literal('public'))

        query = query.add_from(Identifier('information_schema','tables'))
        query = query.where(where_clause)
        cur = self.conn.cursor()
        cur.execute(query.get_query())
        response = [entry[0] for entry in cur.fetchall()]
        cur.close()
        return response
        


class MyFileHandler(DataHandler):

    def __init__(self, filepath: str):
        super().__init__()
        self.filename: str = filepath


class CSVFile(MyFileHandler):
    '''File handler for CSVs.

    File handler that loads and saves in CSV format. Takes a filepath and uses
    that for all IO operations.

    Atributes:
        filepath:
            a string denoting file location for IO operation
    '''
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def open_file(self, **kwargs) -> IO:
        '''Opens file whilst error handling.

        Attempts to a open file, if it is not found or directory does not 
        exist it will then create directory structure then the file.

        Args:
            kwargs:
                Dict of key word arguments to be passed to open

        Returns:
            An opened file at filepath provided.

        Raises:
            Exception:
                An error occurred when opening the file.
        '''
        try:
            file = open(self.filename, **kwargs)
        except FileNotFoundError:
            Path('/'.join(
                self.filename.split('/')[:-1]
                )).mkdir(parents=True, exist_ok=True)
            Path(self.filename).touch(exist_ok=True)
            file = open(self.filename, **kwargs)
        except Exception:
            print("Unexpected error found")
            raise
        return file

    def load(self) -> list[dict]:
        '''Extracts data from a CSV file.

        Returns:
            A list of dictionaries where each element is a row and the keys
            of each dictionary are the headers and value is the data.
        '''
        new_list: list[dict]
        with self.open_file(mode='rt') as file:
            # Implement loading function here
            reader = DictReader(file)
            new_list = [row for row in reader]
        return new_list

    def save(self, input_list: list[dict], template: dict = None) -> bool:
        '''Saves data to a CSV file

        Saves data to a filepath provided in CSV file format. If the list
        is empty and no template is provided then save will fail as no
        information for headers is available.

        Args:
            input_list:
                A list of the rows of data
            template:
                Only the keys are used to create the headers of the file

        Returns:
            A truthy value if saving was successful or falsy if list is empty
            and template is not provided.
        '''
        if len(input_list) < 1 and template is None:
            return False

        with self.open_file(mode='wt') as file:
            column_headers: list
            # Implement saving function here
            if template:
                column_headers = [header for header in template.keys()]
            else:
                column_headers = [header for header in input_list[0].keys()]
            writer = DictWriter(file,
                                fieldnames=column_headers,
                                lineterminator='\r')
            writer.writeheader()
            writer.writerows(input_list)

        return True

    def get_headers(self) -> list[str]:
        '''Retrieves headers of the CSV file

        Returns:
            A list of the headers as strings.
        '''
        header_list: list[str]
        with self.open_file(mode='rt') as file:
            header_row = file.readline()
            header_list = [header.rstrip() for header in header_row.split(',')]

        return header_list
