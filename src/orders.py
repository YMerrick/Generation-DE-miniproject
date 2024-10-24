import os

from .decorators import get_input, menu, print_buffer, print_buffer_exit

dir_path = os.path.dirname(os.path.realpath(__file__))
relative_path = 'data/order_list.txt'

order_list = [
    {
        "customer_name": "John",
        "customer_address": "Unit 2, 12 Main Street, LONDON, WH1 2ER",
        "customer_phone": "0789887334",
        "status": "preparing",
    },
    {
        "customer_name": "Jane",
        "customer_address": "26 North Road, WALSALL, WS6 5MI",
        "customer_phone": "03187622250",
        "status": "done",
    },
    {
        "customer_name": "Joe",
        "customer_address": "21 Church Road, COLCHESTER, CO65 2OC",
        "customer_phone": "03187622250",
        "status": "done",
    },
]

def print_order_menu():
    print("1. Print all orders")
    print("2. Add an order")
    print("3. Update existing order")
    print("4. Delete an order")
    print("0. Return to the main menu")

def clean_key(input: str):
    return input.replace('_', ' ').capitalize()

def print_order(order_item: dict):
    for key, item in order_item.items():
        print(f"{clean_key(key)}: {item}")

@print_buffer_exit
def print_order_list():
    for i, order in enumerate(order_list):
        print(f"{i+1}.")
        print_order(order)
        print()

@print_buffer_exit
def add_order() -> None:
    new_order = {}
    new_order['customer_name'] = get_input("Please enter your customer's name: ")
    new_order['customer_phone'] = get_input("Please enter your customer's phone number: ")
    new_order['customer_address'] = get_input("Please enter your customer's address: ")
    new_order['status'] = 'preparing'
    order_list.append(new_order)

def address_encoder(address: str) -> str:
    return address.replace(',', '_')

def address_decoder(address: str) -> str:
    return address.replace('_', ',')

@print_buffer_exit
def update_order() -> None:
    updated_property: str
    print("0. Exit\n")
    print_order_list()
    # Take input for which order to update
    index_selection = get_input("Please enter the number of the order you would like to select: ", 'int') - 1
    if not index_selection:
        return None
    elif index_selection >= len(order_list) or index_selection < 0:
        print_buffer()
        print("Invalid input, please select a valid id")
        return None
    
    order_selection = order_list[index_selection]

    print_buffer()
    print_order(order_selection)
    print_buffer()

    # Get input for which key they would like to edit
    key_match = get_input("Please enter which property you would like to update: ")
    while not any(filter(lambda key: key_match.lower() in key, order_selection.keys())):
        key_match = get_input("Please enter which property you would like to update: ")
    print_buffer()
    # Search for term in each key
    for key in order_selection.keys():
        if key_match in key:
            updated_property = get_input(f"Please enter what you would like to update it do:\n\n")
            order_selection[key] = updated_property
            break
    print_buffer()
    print_order(order_selection)
    
@print_buffer_exit
def delete_order() -> None:
    print("0. Exit")
    print_order_list()
    user_input = get_input("Please enter the number of the order you would like to delete: ", 'int')
    if not user_input:
        return None
    elif user_input > len(order_list) or user_input < 0:
        print_buffer()
        print("Invalid input, please select a valid id")
        return None
    del order_list[user_input - 1]

def order_menu_choice() -> bool:
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            print_order_list()
        case 2:
            add_order()
        case 3:
            update_order()
        case 4:
            delete_order()
        case 0:
            return False
        case _:
            print("Please select a valid option\n")
    
    return True

@menu
def order_menu() -> bool:
    print_order_menu()
    return order_menu_choice()