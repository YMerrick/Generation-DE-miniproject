import os

from decorators import get_input, menu
from text_file_handler import TextFile

dir_path = os.path.dirname(os.path.realpath(__file__))
relative_path = 'data\\courier_list.txt'

courier_list = TextFile(relative_path).load()

def print_courier_menu():
    pass

def courier_menu_choice():
    pass

@menu
def courier_menu() -> bool:    
    print_courier_menu()
    return courier_menu_choice()