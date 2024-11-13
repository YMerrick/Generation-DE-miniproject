'''CLI application for a cheese mongers.

A command line interface application for a miniproject as part of the 
Generation: You data engineering bootcamp. The program is navigated through
inputting indexes of menu options. 

Usage:

    $ python run.py

TO DO:
    * persist to database
    * database to csv
    *   
'''
from os import getenv

from dotenv import load_dotenv
import psycopg2 as psycopg

from src import get_input, print_buffer, \
    CSVListMenu, MyFileHandler, CSVFile, DictDataManager

# TO DO:
# use loom

# PRINT main menu options GET user input for main menu option

prod_handler = CSVFile('data/product_list.csv')
prod_data = DictDataManager(prod_handler.load())
prod_template = dict.fromkeys(prod_handler.get_headers())
prod_menu = CSVListMenu('product', prod_data, prod_template)

cour_handler = CSVFile('data/courier_list.csv')
cour_data = DictDataManager(cour_handler.load())
cour_template = dict.fromkeys(cour_handler.get_headers())
courier_menu = CSVListMenu('courier', cour_data, cour_template)

order_handler = CSVFile('data/order_list.csv')
order_data = DictDataManager(order_handler.load())
order_template = dict.fromkeys(order_handler.get_headers())
ord_menu = CSVListMenu('order', order_data, order_template)

handler_list = [prod_handler, cour_handler, order_handler]

data_list = [prod_data, cour_data, order_data]

menu_list = [prod_menu, courier_menu, ord_menu]


def save(handler: MyFileHandler, input_list: DictDataManager):
    return handler.save(input_list.get_data())


def save_all(handler_list: list[MyFileHandler],
             data_list: list[DictDataManager]):
    return all(map(save, handler_list, data_list))


def print_main_menu():
    print(
        "1. Products Menu\n"
        "2. Courier Menu\n"
        "3. Orders Menu\n"
        "0. Exit"
    )


def main_menu_choice(menu_list: list[CSVListMenu],
                     handler_list: list[MyFileHandler],
                     data_list: list[DictDataManager]) -> bool:
    print("\nPlease enter a number to select your menu choice:\n")
    user_input = get_input("> ", 'int')
    print_buffer()
    match user_input:
        case choice if 0 < choice <= len(menu_list):
            menu_list[choice - 1].start()
        case 0:
            save_all(handler_list, data_list)
            return False
        case _:
            print("Please select a valid option\n")
    return True


def menu(menu_list, handler_list: list[MyFileHandler],
         data_list: list[DictDataManager]):
    print_main_menu()
    return main_menu_choice(menu_list, handler_list, data_list)


def main():
    print_buffer()
    print("Welcome to York's Fromage Frenzy")
    print_buffer()
    while (rerun := menu(menu_list, handler_list, data_list)):
        pass


if __name__ == "__main__":
    main()
