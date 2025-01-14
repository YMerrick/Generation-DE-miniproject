import os
import sys

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.sql import SQL, Identifier, Literal
from psycopg2.extras import execute_values, LoggingCursor, LoggingConnection
from tabulate import tabulate

from src import Composer, DBHandler, DBDatamanager

load_dotenv()

env_var = {
    'host' : os.getenv('POSTGRES_HOST'),
    'user' : os.getenv('POSTGRES_USER'),
    'dbname' : os.getenv('POSTGRES_DB'),
    'password' : os.getenv('POSTGRES_PASSWORD')
}


def compose_eq(operand1, operand2):
    return SQL('{} = {}').format(operand1, operand2)


def compose_joins(source, dest):
    return SQL('{} = {}').format(source, dest)


def compose_join(dest_table, joins):
    return SQL('{} on {}').format(dest_table, joins)


def add_join(query, join_stmt):
    return SQL('{} JOIN {}').format(query, join_stmt)


def my_format(keyword, before, after):
    stmt = f"{{}} {keyword} {{}}"
    return SQL(stmt).format(before, after)

conn: connection = psycopg2.connect(**env_var)

cur: cursor = conn.cursor()

# table = Identifier('information_schema', 'table_constraints')

# dest_table = Identifier('information_schema','key_column_usage')

# a_dest_table = Identifier('information_schema','constraint_column_usage')

# fields = SQL(' , ').join([Identifier(*table.strings, 'table_name'), Identifier(*dest_table.strings, 'column_name'), Identifier(*a_dest_table.strings, 'table_name'), Identifier(*a_dest_table.strings, 'column_name')])

# print(f"{fields=}\n")

# link = compose_joins(Identifier(*table.strings,'constraint_name'), Identifier(*dest_table.strings, 'constraint_name'))

# anotherLink = compose_joins(Identifier(*table.strings,'table_schema'), Identifier(*dest_table.strings, 'table_schema'))

# joins = SQL(' AND ').join([link,anotherLink])
# # Composes Join clause
# join_clause = compose_join(dest_table,  joins)

# select_portion = add_join(SQL("select {} from {table}").format(fields, table=table),join_clause)

# penultimate = add_join(select_portion,
#                        compose_join(a_dest_table,
#                                     compose_joins(Identifier(*table.strings,'constraint_name'),
#                                                   Identifier(*a_dest_table.strings, 'constraint_name'))
#                                         )
#                             )

# first_check = my_format('=', Identifier(*table.strings, 'constraint_type'), Literal('FOREIGN KEY'))
# second_check = my_format('=', Identifier(*table.strings, 'table_schema'), Literal('public'))

# final_query = my_format('WHERE', penultimate, my_format('AND', first_check, second_check))

# con_logger = LoggingConnection(dsn=" ".join(f"{k}={v}" for k,v in env_var.items()))

# con_logger.initialize(sys.stdout)
# logger = LoggingCursor(con_logger)

# # print(f"{logger=}\n")

# # print(f"{fields=}\n")
# # print(f"{query=}\n")

# cur.execute(final_query)
# print(cur.fetchall())
# # Identifier throws attribute error with string when more than one exists

# cur.execute(SQL("select 1 from customer_table where name = 'John'"))
# print(cur.fetchone())
# logger.close()
# con_logger.close()

# query = Composer('select')
# query.add_field(
#     Identifier('column_name')
#     ).add_from(
#         Identifier('information_schema','columns')
#         ).where(
#             Composer.eq_stmt(
#                 Identifier('table_name'),
#                 Literal('orders')
#                 )
#             )

# cur.execute(query.get_query())
# print(cur.fetchall())

# sql = Composer('select')
# sql.dml = Composer.my_format('', sql.dml, SQL('*'))
# sql.add_from(Identifier('orders'))
# cur.execute(sql.get_query())
# print(cur.fetchall())

# products = DBDatamanager(cur, 'product_table')

# data = products.get(['product_id','name', 'price'])

# print(tabulate(data,
#                headers={k: k.capitalize() for k in data[0].keys()}
#             ))

ccu = Identifier('information_schema', 'constraint_column_usage')
a = Composer.my_format('as', Identifier(*ccu.strings, 'column_name'),
                               Literal('foreign_column_name'))
print(a)

cur.close()

conn.close()


