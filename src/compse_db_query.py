from typing import Self

from psycopg2.sql import SQL, Literal, Composable

class Composer():

    def __init__(self, dml: str):

        match dml.lower():
            case arg if arg in self._commands:
                self.dml = self._commands[arg]()
            case _:
                # Error somehow or reject statement
                pass

        self._commands = {
            'select' : self.__select,
            'insert' : self.__insert,
            'update' : self.__update,
            'delete' : self.__delete
        }

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
        return SQL('{} = {}').format(column, Literal(field))
    
    @staticmethod
    def on(table: Composable, clause: Composable) -> SQL:
        return SQL('{} ON {}').format(table, clause)
    
    @staticmethod
    def my_format(keyword: str, before: Composable, after: Composable) -> SQL:
        stmt = f"{{}} {keyword} {{}}"
        return SQL(stmt).format(before, after)
    
    def into(self, table: Composable) -> Self:
        self.dml = Composer.my_format(self.into.__name__.upper(), self.dml, table)
        return self
    
    def add_from(self, table: Composable) -> Self:
        self.dml = Composer.my_format('FROM', self.dml, table)
        return self
    
    def join(self, clause: Composable) -> Self:
        self.dml = Composer.my_format(self.join.__name__.upper(), self.dml, clause)
        return self
    
    def where(self, clause: Composable) -> Self:
        self.dml = Composer.my_format(self.where.__name__.upper(), self.dml, clause)
        return self

    def make_fields(self, *fields: Composable):
        self.dml = SQL(' , ').join(fields)
        return self
