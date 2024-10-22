from functools import wraps

from .text_file_handler import TextFile
from .product import relative_path, product_list, dir_path

def get_num_input(prompt: str) -> int:
    input_flag = True
    while input_flag:
        if (user_input := input(prompt)).isnumeric():
            input_flag = False
    return int(user_input)

def save_to_file():
    with TextFile(relative_path) as fh:
        fh.save(product_list)

def get_from_file() -> list[str]:
    product_list = []
    with open(f'{dir_path}\\{relative_path}', 'r') as file:
        for line in file:
            product_list.append(line.rstrip())
    return product_list

def get_input(prompt: str, input_type: str = 'str'):
    def decorator_get_input(func):
        @wraps(func)
        def wrapper_get_input():
            if input_type not in ['str','int']:
                raise TypeError("Please use either 'str' or 'int'")
            match input_type:
                case 'int':
                    user_input = get_num_input(prompt)
                case 'str':
                    user_input = input(prompt)
            return func(user_input)
        return wrapper_get_input
    return decorator_get_input

def num_input(prompt: str):
    def decorator_num_input(func):
        @wraps(func)
        # Wraps the function that gets passed
        def wrapper_num_input():
            user_input: int = get_num_input(prompt)
            # This returns the function called with the user_input passed to it
            return func(user_input)
        # Returns the reference to the wrapper which has the original function called
        # When the wrapper is called the it runs the function wrapper and then runs the original functions
        return wrapper_num_input
    return decorator_num_input