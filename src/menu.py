"""Menu class for cheese mongers CLI app.

Class 
Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Usage example:

  foo = CSVListMenu()
  foo.start()

TO DO:
    * Finish module doc string
    * Finish class doc string
    * Finish method doc strings
    * Add better printing options
"""
from abc import ABC, abstractmethod
from typing import Callable

from tabulate import tabulate

from .decorators import get_input, print_buffer, print_buffer_exit
from .data_manager import DataManagerInterface, DictDataManager, DBDatamanager


class Menu(ABC):
    '''Abstract menu interface.

    This is an interface to be sub-classed and implement all abstract methods.
    This is also where the start method is described to create a loop for the
    menu until you exit.

    Atributes:
        context:
            A string describing what the menu is for.
        data:
            A DataManger instance handling our data
    '''
    def __init__(self,  context: str, input_data: DataManagerInterface):
        '''Initialises the instance based on context with data also passed.
        
        Args:
            context (str):
                A single word description of the data
            input_data:
                A DataMangerInterface sub-class instance
        '''
        super().__init__()
        self.context = context
        self.data = input_data

    def print_menu(self):
        print(
            f"1. Print all {self.context}s\n"
            f"2. Add {self.context}\n"
            f"3. Update existing {self.context}\n"
            f"4. Delete {self.context}\n"
            f"5. More print options\n"
            f"0. Return to the main menu\n"
        )

    def validate_user_selection(self,
                                user_selection: int,
                                function: Callable,
                                *args: Callable):
        '''Validates user input then runs function with it's params
        
        Calls a function after validating user input is within bounds then
        passes implicity run functions.
        
        Args:
            user_selection:
                User selection of options provided.
            function:
                Main function you want to call.
            args:
                List of callables.

        Returns:
            Returns a truthy value if call was successful or falsy value if
            user selection is out of bounds or 0.

        Raises:
            TypeError:
                An error occurred calling args.
        '''
        if user_selection > self.data.get_length() or user_selection < 0:
            print("Invalid input, please select a valid id")
            return False
        if not user_selection:
            return False

        function(user_selection, *[function() for function in args])
        return True

    @print_buffer_exit
    def get_user_selection(self) -> int:
        print(f"Enter the number of the {self.context}:\n")
        user_selection = get_input("> ", 'int')

        return user_selection

    @abstractmethod
    def print_entries(self):
        raise NotImplementedError()

    @abstractmethod
    def menu_choice(self):
        raise NotImplementedError()

    def start(self):
        self.print_menu()
        while self.menu_choice():
            self.print_menu()


class DBMenu(Menu):

    def __init__(self, context: str,
                 data: DBDatamanager):
        super().__init__(context, data)

    def print_entries(self):
        '''Ask user for filters then prints listings'''
        return super().print_entries()
    
    def menu_choice(self) -> bool:
        print("\nPlease enter a number to select your menu choice:\n")
        user_input = get_input("> ", 'int')
        print_buffer()
        match user_input:
            case 1:
                'Gets data then prints it out'
                self.print_entries()
            case 2:
                self.add()
            case 3:
                self.print_entries()
                print("Enter 0 to EXIT\n")
                self.validate_user_selection(
                    self.get_user_selection(),
                    self.update,
                    self.get_property,
                    self.get_new_property_value
                    )
            case 4:
                self.print_entries()
                print("Enter 0 to EXIT\n")
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



class CSVListMenu(Menu):
    '''Menu for list of dictionaries.

    This is an interface to be sub-classed and implement all abstract methods.
    This is also where the start method is described to create a loop for the
    menu until you exit.

    Atributes:
        template:

    '''
    def __init__(self, context: str,
                 data: DictDataManager,
                 template: dict = None):
        ''''''
        if data.get_length() < 1 and template is None:
            raise ValueError("List is empty or template not passed")

        super().__init__(context, data)
        if template is None:
            # Make the template
            self.template = dict.fromkeys(data.get_keys())
        else:
            self.template = template

    def clean_key(self, input: str) -> str:
        '''Cleans key for string output
        
        Args:
            input:
                The string to be modified
                
        Returns:
            A string where underscores are replaced and first letter is
            capitalised.
        '''
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

    def print_table(self, data: list[dict]):
        if not data:
            keys = self.template.keys()
        else:
            keys = data[0].keys()
        tabular_form = tabulate(data,
                                headers={k: self.clean_key(k) for k in keys},
                                showindex=range(1, len(data)+1),
                                floatfmt='.2f',
                                tablefmt='rounded_grid',
                                )
        print(tabular_form)

    def menu_print(self):
        print(
            "1. Search for Item in a column\n"
            "2. Select columns to display\n"
            "0. Return to previous menu\n"
        )

    def search(self):
        # Selects column and then enter search term
        # Then prints returned data
        columns: list = [{'columns': i} for i in self.data.get_keys()]
        self.print_table(columns)
        print('Please enter the number of the column for selection:\n')
        user_selection = get_input("> ", 'int')
        print('Please enter your search term:\n')
        search_term = get_input("> ")
        return_data = self.data.filter_on_column(columns.pop(user_selection - 1)['columns'], search_term)
        if not return_data:
            print("That column does not exist\nReturning to menu")
            return
        self.print_table(return_data)

    def select_columns(self):
        # Select columns to be displayed
        print('Enter nothing to finalise selection')
        columns: list = [{'columns': i} for i in self.data.get_keys()]
        user_selection: list = []
        self.print_table(columns)
        # Keeps looping asking for columns until its matched the length or empty string is returned
        while (user_input := get_input('Please enter the number of the columns you would like to select\n\n> ')):
            user_input = int(user_input)
            user_selection.append(columns.pop(user_input - 1)['columns'])
            self.print_table(columns)
        printing_data = self.data.select_columns(*user_selection)
        if not printing_data:
            print('You have selected nothing.\nReturning to menu')
        self.print_table(printing_data)

    def menu_print_choice(self):
        print("Please enter a number to select your menu choice:\n")
        user_input = get_input("> ", 'int')
        match user_input:
            case 1:
                self.search()
            case 2:
                self.select_columns()
            case 0:
                return False
            case _:
                print("Please select a valid option")
                print_buffer()
        return True

    @print_buffer_exit
    def print_entries(self):
        # Adds extra print options and mini menu for it
        self.menu_print()
        while self.menu_print_choice():
            self.menu_print()

    def add(self):
        new_dict = {}
        for key in self.template:
            match key.lower():
                case 'status':
                    new_dict[key] = 'preparing'
                case _:
                    new_dict[key] = get_input(
                        f"Please enter your {self.clean_key(key)}:\n> "
                        )
        self.data.add(new_dict)

    def list_keys_from_search(self, search_term: str):
        return list(filter(lambda key: search_term.lower() in key,
                           self.template.keys()))

    def get_property(self,) -> str:
        print("Enter which property you would like to select:\n ")
        key_match = get_input("> ")
        while not (keys := self.list_keys_from_search(key_match)):
            key_match = get_input(
                "Enter which property you would like to select:\n> "
                )
        return keys[0]

    def get_new_property_value(self) -> str:
        print("\nEnter new the new property:\n")
        return get_input("> ")

    def update(self, user_selection: int,
               property_selected: str,
               updated_property: str):
        update_dict = self.data.update(user_selection,
                                       property_selected,
                                       updated_property)
        self.print_table([update_dict])

    def delete(self, user_selection: int):
        removed_element = self.data.delete_element(user_selection)
        self.print_table([removed_element])
        print("The above entry been DELETED!\n")

    def menu_choice(self) -> bool:
        print("Please enter a number to select your menu choice:\n")
        user_input = get_input("> ", 'int')
        print_buffer()
        match user_input:
            case 1:
                self.print_table(self.data.get_data())
            case 2:
                self.add()
            case 3:
                self.print_table(self.data.get_data())
                print("Enter 0 to EXIT\n")
                self.validate_user_selection(
                    self.get_user_selection(),
                    self.update,
                    self.get_property,
                    self.get_new_property_value
                    )
            case 4:
                self.print_table(self.data.get_data())
                print("Enter 0 to EXIT\n")
                self.validate_user_selection(
                    self.get_user_selection(),
                    self.delete
                    )
            case 5:
                self.print_entries()
            case 0:
                return False
            case _:
                print("Please select a valid option")
                print_buffer()

        return True
