from abc import ABC, abstractmethod
from typing import Callable

from src import get_input, print_buffer, print_buffer_exit
from src import DataManagerInterface, DictDataManager, StrListDataManager

class Menu(ABC):

    def __init__(self,  context: str, input_data: DataManagerInterface):
        super().__init__()
        self.context = context
        self.data = input_data

    def print_menu(self):
        print(
            f"1. Print all {self.context}s\n"
            f"2. Add {self.context}\n"
            f"3. Update existing {self.context}\n"
            f"4. Delete {self.context}\n"
            f"0. Return to the main menu"
        )
    
    def validate_user_selection(self, user_selection: int, function: Callable, *args: Callable):
        # Implicitly running other functions when not 0
        # *args are callables
        if user_selection > self.data.get_length() or user_selection < 0:
            return False
        if not user_selection:
            return False
        
        function(user_selection, *[function() for function in args])
        return True

    @print_buffer_exit
    def get_user_selection(self) -> int:
        print("0. Exit")
        self.print_list()
        print(f"Enter the number of the {self.context}:\n")
        user_selection = get_input("> ", 'int')

        if user_selection > self.data.get_length() or user_selection < 0:
            print("Invalid input, please select a valid id")

        
        return user_selection

    @abstractmethod
    def print_list(self):
        raise NotImplementedError()

    @abstractmethod
    def menu_choice(self):
        raise NotImplementedError()

    def start(self):
        self.print_menu()
        while (value := self.menu_choice()):
            self.print_menu()

class StringListMenu(Menu):

    def __init__(self, context, input_data: StrListDataManager):
        super().__init__(context, input_data)

    @print_buffer_exit
    def print_list(self, **kwargs) -> None:
        for i, element in enumerate(self.data.get_data()):
            print(f"{i+1}. {element}", **kwargs)
        
    @print_buffer_exit
    def get_new_item(self):
        print(f"Enter the new {self.context}:\n")
        return get_input('> ')

    @print_buffer_exit
    def add(self, user_item: str) -> None:
        self.data.add(user_item)
        print(f"{user_item} has been added!")
    
    @print_buffer_exit
    def update(self, user_selection: int, updated_item: str) -> None:
        self.data.update(user_selection, updated_item)
        print("The listing has been updated")

    @print_buffer_exit
    def delete_element(self, user_selection: int) -> None:
        print(f"{self.data.delete_element(user_selection)} has been deleted!")

    def menu_choice(self) -> bool:
        user_input = get_input("Please enter a number to select your menu choice:\n> ",'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_list()
            case 2:
                self.add(self.get_new_item())
            case 3:
                self.validate_user_selection(self.get_user_selection(), self.update, self.get_new_item)
            case 4:
                self.validate_user_selection(self.get_user_selection(), self.delete_element)
            case 0:
                return False
            case _:
                print("Please select a valid option\n")

        return True

class CSVListMenu(Menu):

    def __init__(self, context: str, input_list: DictDataManager, template: dict = None):
        if input_list.get_length() < 1 and template is None:
            raise ValueError("List is empty or template not passed")
        
        super().__init__(context, input_list)
        if template is None:
            # Make the template
            self.template = dict.fromkeys(input_list.get_keys())
        else:
            self.template = template
    
    def clean_key(self, input: str) -> str:
        return input.replace('_', ' ').capitalize()
    
    def print_dict(self, dictionary: dict):
        for key, value in dictionary.items():
            match key:
                # case key if 'address' in key:
                case _:
                    print(f"{self.clean_key(key)}: {value}")

    @print_buffer_exit
    def print_list(self):
        for index, element in enumerate(self.data.get_data()):
            print(f"{index+1}.")
            self.print_dict(element)
            print()
    
    def add(self):
        new_dict = {}
        for key in self.template:
            new_dict[key] = get_input(f"Please enter your {self.clean_key(key)}:\n> ")
        self.data.add(new_dict)
    
    def get_property(self,):
        key_match = get_input("Enter which property you would like to select:\n> ")
        while not (keys := list(filter(lambda key: key_match.lower() in key, self.template.keys()))):
            key_match = get_input("Enter which property you would like to select:\n> ")
        return keys[0]
    
    def get_new_property_value(self):
        print(f"Enter new the new property:\n")
        return get_input("> ")
    
    def update(self, user_selection: int, property_selected: str, updated_property: str):
        update_dict = self.data.update(user_selection, property_selected, updated_property)
        # Print updated dictionary
    
    def delete(self, user_selection: int):
        removed_element = self.data.delete_element(user_selection - 1)
        self.print_dict(removed_element)
        print(f"\nHas been deleted!")
    
    def menu_choice(self):
        user_input = get_input("Please enter a number to select your menu choice:\n> ",'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_list()
            case 2:
                self.add()
            case 3:
                self.validate_user_selection(
                    self.get_user_selection(), 
                    self.update, 
                    self.get_property,
                    self.get_new_property_value
                    )
            case 4:
                self.validate_user_selection(
                    self.get_user_selection(), 
                    self.delete
                    )
            case 0:
                return False
            case _:
                print("Please select a valid option")
                print_buffer()

        return True
    