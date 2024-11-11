from abc import ABC, abstractmethod
from typing import Callable

from tabulate import tabulate

from .decorators import get_input, print_buffer, print_buffer_exit
from .data_manager import DataManagerInterface, DictDataManager

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

class CSVListMenu(Menu):

    def __init__(self, context: str, data: DictDataManager, template: dict = None):
        if data.get_length() < 1 and template is None:
            raise ValueError("List is empty or template not passed")
        
        super().__init__(context, data)
        if template is None:
            # Make the template
            self.template = dict.fromkeys(data.get_keys())
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

    @print_buffer_exit
    def print_table(self, data: list[dict]):
        if not data:
            keys = self.template.keys()
        else:
            keys = data[0].keys()
        tabular_form = tabulate(data,
                                headers= {k: self.clean_key(k) for k in keys}, 
                                showindex= range(1, len(data)+1),
                                floatfmt='.2f',
                                tablefmt='rounded_grid',
                                )
        print(tabular_form)

    def add(self):
        new_dict = {}
        for key in self.template:
            match key.lower():
                case 'status':
                    new_dict[key] = 'preparing'
                case _:
                    new_dict[key] = get_input(f"Please enter your {self.clean_key(key)}:\n> ")
        self.data.add(new_dict)

    def get_property(self,) -> str:
        print("Enter which property you would like to select:\n ")
        key_match = get_input("> ")
        while not (keys := list(filter(lambda key: key_match.lower() in key, self.template.keys()))):
            key_match = get_input("Enter which property you would like to select:\n> ")
        return keys[0]

    def get_new_property_value(self) -> str:
        print(f"\nEnter new the new property:\n")
        return get_input("> ")

    def update(self, user_selection: int, property_selected: str, updated_property: str):
        update_dict = self.data.update(user_selection, property_selected, updated_property)
        self.print_table([update_dict])

    def delete(self, user_selection: int):
        removed_element = self.data.delete_element(user_selection)
        self.print_table([removed_element])
        print(f"The above entry been DELETED!\n")

    def menu_choice(self) -> bool:
        print("\nPlease enter a number to select your menu choice:\n")
        user_input = get_input("> ",'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_table(self.data.get_data())
            case 2:
                self.add()
            case 3:
                self.print_table(self.data.get_data())
                print(f"Enter 0 to EXIT\n")
                self.validate_user_selection(
                    self.get_user_selection(), 
                    self.update, 
                    self.get_property,
                    self.get_new_property_value
                    )
            case 4:
                self.print_table(self.data.get_data())
                print(f"Enter 0 to EXIT\n")
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
