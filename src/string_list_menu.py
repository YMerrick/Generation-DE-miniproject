# CREATE products list
from .decorators import menu, get_input, print_buffer, print_buffer_exit
from .text_file_handler import TextFile

def print_menu(context: str):
    print(f"1. List all {context}s")
    print(f"2. Add {context}")
    print(f"3. Update existing {context}")
    print(f"4. Delete {context}")
    print(f"0. Return to the main menu")

@print_buffer_exit
def print_list(input_list: list[str]):
    for i, element in enumerate(input_list):
        print(f"{i+1}. {element}")

@print_buffer_exit
def add(input_list: list, context: str):
    print(f"Enter the new {context}:\n")
    input_list.append(get_input('> '))
    
@print_buffer_exit
def update(input_list: list, context: str) -> None:
    print("0. Exit")
    print_list(input_list)
    print(f"Enter the number of the {context}:\n")
    product_number = get_input("> ", 'int') - 1
    print_buffer()
    if product_number == -1:
        return None
    elif product_number >= len(input_list) or product_number < -1:
        print("Invalid input, please select a valid id")
        return None
    
    print(f"Enter the new {context}:\n")
    updated_product = get_input("> ")
    print_buffer()
    input_list[product_number] = updated_product
    print("The listing has been updated")

@print_buffer_exit
def delete(input_list: list, context: str) -> None:
    print("0. Exit")
    print_list(input_list)
    print(f"Enter the number of the {context}:\n")
    user_input = get_input('> ', 'int')
    # If user_input is 0 then exits
    if not user_input:
        return None
    elif user_input > len(input_list) or user_input < 0:
        print("Invalid input, please select a valid id")
        return None
    input_list.pop(user_input - 1)

def menu_choice(file_handler: TextFile, input_list: list[str], context: str) -> bool:
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            print_list(input_list)
        case 2:
            add(input_list, context)
        case 3:
            update(input_list, context)
        case 4:
            delete(input_list, context)
        case 0:
            file_handler.save(input_list)
            return False
        case _:
            print("Please select a valid option\n")

    file_handler.save(input_list)
    return True

@menu
def menu_start(context,/, file_handler: TextFile, input_list: list[str]) -> bool:
    print_menu(context)
    return menu_choice(file_handler, input_list, context)
