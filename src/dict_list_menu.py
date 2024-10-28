from decorators import get_input, menu, print_buffer, print_buffer_exit
from csv_file_handler import CSVFile

def print_menu(context: str):
    print(f"1. Print all {context}s")
    print(f"2. Add {context}")
    print(f"3. Update existing {context}")
    print(f"4. Delete {context}")
    print(f"0. Return to the main menu")

def clean_key(input: str) -> str:
    return input.replace('_', ' ').capitalize()

def print_dict(dictionary: dict) -> None:
    for key, item in dictionary.items():
        print(f"{clean_key(key)}: {item}")

@print_buffer_exit
def print_list(input_list: list[dict]) -> None:
    for index, element in enumerate(input_list):
        print(f"{index+1}.")
        print_dict(element)

@print_buffer_exit
def add(input_list: list[dict], template: dict) -> None:
    new_dict = {}
    for key in template:
        new_dict[key] = get_input(f"Please enter your {clean_key(key)}:\n> ")
    input_list.append(new_dict)

def address_encoder(address: str) -> str:
    return address.replace(',', '_')

def address_decoder(address: str) -> str:
    return address.replace('|', ',')

@print_buffer_exit
def update(input_list: list[dict]) -> None:
    updated_property: str
    print("0. Exit\n")
    print_list(input_list)
    # Take input for which order to update
    index_selection = get_input("Please enter the number of the order you would like to select:\n> ", 'int') - 1
    if not index_selection:
        return None
    elif index_selection > len(input_list) or index_selection < 0:
        print("Invalid input, please select a valid id")
        return None
    
    user_selection = input_list[index_selection]

    print_buffer()
    print_dict(user_selection)
    print_buffer()

    # Get input for which key they would like to edit
    key_match = get_input("Please enter which property you would like to update:\n> ")
    while not any(filter(lambda key: key_match.lower() in key, user_selection.keys())):
        key_match = get_input("Please enter which property you would like to update:\n> ")
    print_buffer()
    # Search for term in each key
    for key in user_selection.keys():
        if key_match in key:
            updated_property = get_input(f"Please enter what you would like to update it do:\n> ")
            user_selection[key] = updated_property
            break
    print_buffer()
    print_dict(user_selection)
    
@print_buffer_exit
def delete_element(input_list: list[dict]) -> None:
    print("0. Exit")
    print_list(input_list)
    user_input = get_input("Please enter the number of the order you would like to delete:\n> ", 'int')
    if not user_input:
        return None
    elif user_input > len(input_list) or user_input < 0:
        print_buffer()
        print("Invalid input, please select a valid id")
        return None
    del input_list[user_input - 1]

def menu_choice(input_list: list[dict], file_handler: CSVFile, template: dict) -> bool:
    user_input = get_input("Please enter a number to select your menu choice:\n> ",'int')
    print_buffer()
    match user_input:
        case 1:
            print_list(input_list)
        case 2:
            add(input_list, template)
        case 3:
            update(input_list)
        case 4:
            delete_element(input_list)
        case 0:
            file_handler.save(input_list)
            return False
        case _:
            print("Please select a valid option")
            print_buffer()
    file_handler.save(input_list)
    return True

@menu
def menu_start(context: str,/ ,file_handler: CSVFile, input_list: list[dict], template: dict) -> bool:
    print_menu(context)
    return menu_choice(input_list, file_handler, template)