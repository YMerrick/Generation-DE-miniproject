from functools import wraps

def get_num_input(prompt: str) -> int:
    input_flag = True
    while input_flag:
        if (user_input := input(prompt)).isnumeric():
            input_flag = False
    return int(user_input)

def get_input(prompt:str, input_type: str = 'str'):
    if input_type not in ['str','int']:
        raise TypeError("Please use either 'str' or 'int'")
    match input_type:
        case 'int':
            user_input = get_num_input(prompt)
        case 'str':
            user_input = input(prompt)
    return user_input

def print_buffer_exit(func):
    @wraps(func)
    def wrapper_buffer(*args, **kwargs):
        value = func(*args, **kwargs)
        print_buffer()
        return value
    return wrapper_buffer

def print_buffer() -> None:
    star_line = "*" * 60
    print(f"\n{star_line}\n")

def menu_loop(func):
    '''Requires functions decorate to return a truthy value'''
    @wraps(func)
    def wrapper_menu(*args, **kwargs):
        rerun_flag = True
        while rerun_flag:
            rerun_flag = func(*args, **kwargs)
    return wrapper_menu 