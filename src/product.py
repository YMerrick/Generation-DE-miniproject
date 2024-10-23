# CREATE products list
import os

from .decorators import menu, get_input, print_buffer, print_buffer_exit
from .text_file_handler import TextFile

dir_path = os.path.dirname(os.path.realpath(__file__))
relative_path = 'data/product_list.txt'

product_list = TextFile(relative_path).load()

def print_product_menu():
    print("1. List all products")
    print("2. Add product to catalog")
    print("3. Update existing product")
    print("4. Delete product from catalog")
    print("0. Return to the main menu")

@print_buffer_exit
def print_product_list():
    for i, product in enumerate(product_list):
        print(f"{i+1}. {product}")

@print_buffer_exit
def add_product():
    global product_list
    user_input = get_input("Please enter a product to add to the catalog: ")
    product_list.append(user_input)
    
@print_buffer_exit
def update_product() -> None:
    # Split user input into different functions
    print("0. Exit")
    print_product_list()
    product_number = get_input("Please enter the number of the product you would like to select: ", 'int') - 1
    print_buffer()
    if product_number == -1:
        return None
    elif product_number >= len(product_list) or product_number < -1:
        print("Invalid input, please select a valid id")
        return None
    
    updated_product = get_input("Please enter what you would like to update the product to: ")
    print_buffer()
    product_list[product_number] = updated_product
    print("The product listing has been updated")

def delete_product() -> None:
    print("0. Exit")
    print_product_list()
    user_input = get_input("Please enter the number of the product you would like to select: ", 'int')
    print_buffer()
    # If user_input is 0 then exits
    if not user_input:
        return None
    elif user_input >= len(product_list) or user_input < 0:
        print("Invalid input, please select a valid id")
        return None
    product_list.pop(user_input - 1)

def product_menu_choice() -> bool:
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            print_product_list()
            print()
        case 2:
            add_product()
        case 3:
            update_product()
        case 4:
            delete_product()
        case 0:
            TextFile(relative_path, 'wt').save(product_list)
            return False
        case _:
            print("Please select a valid option\n")

    TextFile(relative_path, 'wt').save(product_list)
    return True

@menu
def product_menu() -> bool:
    print_product_menu()
    return product_menu_choice()
