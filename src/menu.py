from abc import ABC, abstractmethod

from .decorators import get_input, print_buffer, print_buffer_exit
from .text_file_handler import TextFile

class Menu(ABC):

    @abstractmethod
    def print_menu(self, context: str):
        print(
            f"1. Print all {context}s\n"
            f"2. Add {context}\n"
            f"3. Update existing {context}\n"
            f"4. Delete {context}\n"
            f"0. Return to the main menu"
        )

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
    def get_new_item(self):
        print(f"Enter the new {self.context}:\n")
        return get_input('> ')
        
    @print_buffer_exit
    def get_user_selection(self) -> int:
        print("0. Exit")
        self.print_list()
        print(f"Enter the number of the {self.context}:\n")
        user_selection = get_input("> ", 'int')

        if user_selection > len(self.user_list) or user_selection < 0:
            print("Invalid input, please select a valid id")
            raise IndexError
        
        return user_selection

    @print_buffer_exit
    def add(self, user_item: str) -> None:
        self.user_list.append(user_item)
        print(f"{user_item} has been added!")
    
    @print_buffer_exit
    def update(self, user_selection: int, updated_item: str) -> None:
        self.user_list[user_selection - 1] = updated_item
        print("The listing has been updated")

    @print_buffer_exit
    def delete_element(self, user_selection: int) -> None:
        print(f"{self.user_list.pop(user_selection - 1)} has been deleted!")

    def validate_user_selection(self, user_selection: int, function, *args):
        if user_selection:
            function(user_selection, *args)
        return True if user_selection else False

    def menu_choice(self) -> bool:
        user_input = get_input("Please enter a number to select your menu choice:\n> ",'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_list()
            case 2:
                self.add(self.get_new_item())
            case 3:
                self.validate_user_selection(self.get_user_selection(), self.update, self.get_new_item())
            case 4:
                self.validate_user_selection(self.get_user_selection(), self.delete_element)
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