from src.decorators import get_input, menu, print_buffer
from src.orders import order_menu
from src.string_list_menu import menu_start
from src.text_file_handler import TextFile
from src.menu import StringListMenu

# TO DO:
# Implement order functions
# use loom
# 

# PRINT main menu options GET user input for main menu option

prod_handler = TextFile('data/product_list.txt')
prod_list = prod_handler.load()
prod_menu = StringListMenu('product', prod_handler, prod_list)

cour_handler = TextFile('data/courier_list.txt')
cour_list = cour_handler.load()
courier_menu = StringListMenu('courier', cour_handler, cour_list)

def print_main_menu():
    print(
        "1. Products Menu\n" 
        "2. Courier Menu\n" 
        "3. Orders Menu\n" 
        "0. Exit"
    )

def main_menu_choice() -> bool:
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            prod_menu.start()
        case 2:
            courier_menu.start()
        case 3:
            order_menu()
        case 0:
            return False
        case _:
            print("Please select a valid option\n")
    return True

@menu
def main():
    print_main_menu()
    return main_menu_choice()

# IF user input is 0: EXIT app

if __name__ == "__main__":
    print_buffer()
    print("Welcome to York's Fromage Frenzy")
    print_buffer()
    main()
