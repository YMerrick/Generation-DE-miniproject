import os

from .decorators import get_input, menu, print_buffer, print_buffer_exit
from .text_file_handler import TextFile

dir_path = os.path.dirname(os.path.realpath(__file__))
relative_path = 'data/courier_list.txt'

courier_list = TextFile(relative_path).load()

@print_buffer_exit
def print_courier_list() -> None:
    for i, product in enumerate(courier_list):
        print(f"{i+1}. {product}")

@print_buffer_exit
def add_courier() -> None:
    global courier_list
    user_input = get_input("Please enter the name of the courier to add: ")
    courier_list.append(user_input)

@print_buffer_exit
def update_courier() -> None:
    print("0. Exit")
    print_courier_list()
    product_number = get_input("Please enter the number of the courier you would like to select: ", 'int') - 1
    print_buffer()
    if product_number == -1:
        return None
    elif product_number >= len(courier_list) or product_number < -1:
        print("Invalid input, please select a valid id")
        return None
    
    updated_product = get_input("Please enter what you would like to update the courier information to: ")
    print_buffer()
    courier_list[product_number] = updated_product
    print("The product listing has been updated")

@print_buffer_exit
def delete_courier() -> None:
    print("0. Exit")
    print_courier_list()
    user_input = get_input("Please enter the number of the product you would like to select: ", 'int')
    print_buffer()
    # If user_input is 0 then exits
    if not user_input:
        return None
    elif user_input >= len(courier_list) or user_input < 0:
        print("Invalid input, please select a valid id")
        return None
    courier_list.pop(user_input - 1)

def print_courier_menu():
    print("1. List all couriers")
    print("2. Add a courier")
    print("3. Update existing courier information")
    print("4. Delete courier")
    print("0. Return to the main menu")

def courier_menu_choice():
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            print_courier_list()
        case 2:
            add_courier()
        case 3:
            update_courier()
        case 4:
            delete_courier()
        case 0:
            with TextFile(relative_path) as fh:
                fh.save(courier_list)
            return False
        case _:
            print("Please select a valid option\n")
    with TextFile(relative_path) as fh:
        fh.save(courier_list)
    return True

@menu
def courier_menu() -> bool:    
    print_courier_menu()
    return courier_menu_choice()