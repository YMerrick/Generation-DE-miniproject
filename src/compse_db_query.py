from typing import Self, Iterable

from psycopg2.sql import SQL, Composable, Composed

class Composer():

    def __init__(self, dml: str):

        self.__commands = {
            'select' : self.__select,
            'insert' : self.__insert,
            'update' : self.__update,
            'delete' : self.__delete
        }

        match dml.lower():
            case arg if arg in self.__commands:
                self.dml = self.__commands[arg]()
            case _:
                # Error somehow or reject statement
                pass

    def __select(self) -> SQL:
        return SQL('SELECT')

    def __insert(self) -> SQL:
        return SQL('INSERT')

    def __update(self) -> SQL:
        return SQL('UPDATE')

    def __delete(self) -> SQL:
        return SQL('DELETE')
    
    @staticmethod
    def eq_stmt(column: Composable, field: Composable) -> SQL:
        return SQL('{} = {}').format(column, field)
    
    @staticmethod
    def on(table: Composable, clause: Composable) -> SQL:
        return SQL('{} ON {}').format(table, clause)
    
    @staticmethod
    def my_format(keyword: str,
                  before: Composable,
                  after: Composable) -> SQL:
        stmt = f"{{}} {keyword} {{}}"
        return SQL(stmt).format(before, after)
    
    def add_field(self, field: Composable) -> Self:
        self.dml = SQL('{} {}').format(self.dml,
                                       field)
        return self
    
    def into(self, table: Composable) -> Self:
        self.dml = Composer.my_format(self.into.__name__.upper(),
                                      self.dml, table)
        return self
    
    def add_from(self, table: Composable) -> Self:
        self.dml = Composer.my_format('FROM', self.dml, table)
        return self
    
    def join(self, clause: Composable) -> Self:
        self.dml = Composer.my_format(self.join.__name__.upper(),
                                      self.dml, clause)
        return self
    
    def where(self, clause: Composable) -> Self:
        self.dml = Composer.my_format(self.where.__name__.upper(),
                                      self.dml,
                                      clause)
        return self
    
    def get_query(self) -> Composed:
        return self.dml
    
    def returning(self, field: Composable) -> Self:
        self.dml = Composer.my_format(self.returning.__name__.upper(),
                                      self.dml,
                                      field)
        return self
    
    def values(self, field: Composable) -> Self:
        self.dml = Composer.my_format(self.returning.__name__.upper(),
                                      self.dml,
                                      field)
        return self
        
    def _set(self, field: Composable) -> Self:
        self.dml = Composer.my_format('SET',
                                      self.dml,
                                      field)
        return self

    @staticmethod
    def make_fields(*fields: Composable):
        return SQL(' , ').join(fields)
