from abc import ABC, abstractmethod

from .decorators import get_input, print_buffer, print_buffer_exit
from .text_file_handler import TextFile

class Menu(ABC):

    @abstractmethod
    def print_menu(self, context: str):
        print(f"1. Print all {context}s")
        print(f"2. Add {context}")
        print(f"3. Update existing {context}")
        print(f"4. Delete {context}")
        print(f"0. Return to the main menu")

    @abstractmethod
    def print_list(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def update(self):
        pass
        
    @abstractmethod
    def delete_element(self):
        pass

    @abstractmethod
    def menu_choice(self):
        pass

    @abstractmethod
    def start(self):
        self.print_menu()
        while (value := self.menu_choice()):
            self.print_menu()

class StringListMenu(Menu):

    def __init__(self, context, file_handler: TextFile, input_list: list[str]):
        self.context = context
        self.file_handler = file_handler
        self.user_list = input_list
    
    def print_menu(self):
        return super().print_menu(self.context)

    @print_buffer_exit
    def print_list(self, **kwargs) -> None:
        for i, element in enumerate(self.user_list):
            print(f"{i+1}. {element}", **kwargs)

    @print_buffer_exit
    def add(self) -> None:
        print(f"Enter the new {self.context}:\n")
        self.user_list.append(get_input('> '))
        
    @print_buffer_exit
    def update(self) -> None:
        print("0. Exit")
        self.print_list()
        print(f"Enter the number of the {self.context}:\n")
        product_number = get_input("> ", 'int') - 1
        
        if product_number == -1:
            return None
        elif product_number >= len(self.user_list) or product_number < -1:
            print("Invalid input, please select a valid id")
            return None
        print_buffer()
        print(f"Enter the new {self.context}:\n")
        updated_product = get_input("> ")
        print_buffer()
        self.user_list[product_number] = updated_product
        print("The listing has been updated")

    @print_buffer_exit
    def delete_element(self) -> None:
        print("0. Exit")
        self.print_list()
        print(f"Enter the number of the {self.context}:\n")
        user_input = get_input('> ', 'int')
        # If user_input is 0 then exits
        if not user_input:
            return None
        elif user_input > len(self.user_list) or user_input < 0:
            print("Invalid input, please select a valid id")
            return None
        self.user_list.pop(user_input - 1)

    def menu_choice(self) -> bool:

        user_input = get_input("Please enter a number to select your menu choice: ",'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_list()
            case 2:
                self.add()
            case 3:
                self.update()
            case 4:
                self.delete_element()
            case 0:
                self.file_handler.save(self.user_list)
                return False
            case _:
                print("Please select a valid option\n")

        self.file_handler.save(self.user_list)
        return True
    
    def start(self):
        return super().start()

class CSVListMenu(Menu):

    def __init__(self, context: str, file_handler, input_list: list[dict]):
        self.context = context

    def print_menu(self):
        return super().print_menu(self.context)
    
    def print_list(self):
        return super().print_list()
    
    def add(self):
        return super().add()
    
    def update(self):
        return super().update()
    
    def delete_element(self):
        return super().delete_element()
    
    def menu_choice(self):
        return super().menu_choice()
    
    def start(self):
        return super().start()