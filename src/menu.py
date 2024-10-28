from abc import ABC, abstractmethod

from .decorators import get_input, print_buffer, print_buffer_exit

class Menu(ABC):

    def __init__(self,  context: str, input_list: list):
        super().__init__()
        self.context = context
        self.user_list = input_list

    def print_menu(self):
        print(
            f"1. Print all {self.context}s\n"
            f"2. Add {self.context}\n"
            f"3. Update existing {self.context}\n"
            f"4. Delete {self.context}\n"
            f"0. Return to the main menu"
        )
    
    def validate_user_selection(self, user_selection: int, function, *args):
        if user_selection:
            function(user_selection, *args)
            return True
        return False

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

    @abstractmethod
    def print_list(self):
        raise NotImplementedError()

    @abstractmethod
    def add(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()
        
    @abstractmethod
    def delete_element(self):
        raise NotImplementedError() 

    @abstractmethod
    def menu_choice(self):
        raise NotImplementedError()

    def start(self):
        self.print_menu()
        while (value := self.menu_choice()):
            self.print_menu()

class StringListMenu(Menu):

    def __init__(self, context, input_list: list[str]):
        super().__init__(context, input_list)

    @print_buffer_exit
    def print_list(self, **kwargs) -> None:
        for i, element in enumerate(self.user_list):
            print(f"{i+1}. {element}", **kwargs)
        
    @print_buffer_exit
    def get_new_item(self):
        print(f"Enter the new {self.context}:\n")
        return get_input('> ')

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
                return False
            case _:
                print("Please select a valid option\n")

        return True

class CSVListMenu(Menu):

    def __init__(self, context: str, input_list: list[dict], template: dict = None):
        super().__init__(context, input_list)
        if template is None:
            # Make the template
            self.template = None
        else:
            self.template = template
    
    def clean_key(self, input: str) -> str:
        return input.replace('_', ' ').capitalize()
    
    def print_dict(self, dictionary: dict):
        for key, item in dictionary.items():
            match key:
                case key if 'address' in key:
                    print(f"{self.clean_key(key): {self.address_decoder(item)}}")
                case _:
                    print(f"{self.clean_key(key)}: {item}")

    def print_list(self):
        for index, element in enumerate(self.user_list):
            print(f"{index+1}.")
            self.print_dict(element)
    
    def add(self,):
        new_dict = {}
        for key in self.template:
            new_dict[key] = get_input(f"Please enter your {self.clean_key(key)}:\n> ")
        if any(filter(lambda key: 'address' in key, new_dict.keys())):
            # This does not work
            # Find property and then update it
            for _property in new_dict:
                if 'address' in _property:
                    new_dict[_property] = self.address_encoder(new_dict[_property])
                    break
        self.user_list.append(new_dict)
    
    def address_encoder(address: str) -> str:
        return address.replace(',', '|')

    def address_decoder(address: str) -> str:
        return address.replace('|', ',')
    
    def get_property(self,):
        key_match = get_input("Enter which property you would like to select:\n> ")
        while not any(filter(lambda key: key_match.lower() in key, self.template.keys())):
            key_match = get_input("Enter which property you would like to select:\n> ")
        return key_match
    
    def get_new_property_value(self, property_context):
        print(f"Enter new {property_context}:\n")
        return get_input("> ")
    
    def update(self, user_selection: int, property_selected: str, updated_property: str):
        selected_dict = self.user_list[user_selection - 1]
        selected_dict[property_selected] = updated_property
    
    def delete_element(self, user_selection: int):
        removed_element = self.user_list.pop(user_selection - 1)
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
                    self.get_property(),
                    self.get_new_property_value()
                    )
                self.update()
            case 4:
                self.validate_user_selection(
                    self.get_user_selection(), 
                    self.delete_element
                    )
            case 0:
                # Apply encoder to all addresses
                return False
            case _:
                print("Please select a valid option")
                print_buffer()

        return True
    