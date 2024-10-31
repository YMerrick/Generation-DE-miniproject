from src import get_input, print_buffer, menu_loop, StringListMenu, CSVListMenu, MyFileHandler, TextFile, CSVFile

# TO DO:
# use loom
# 

# PRINT main menu options GET user input for main menu option

prod_handler = CSVFile('data/product_list.csv')
prod_list = prod_handler.load()
prod_template = CSVFile('data/product_template.csv').load()[0]
prod_menu = CSVListMenu('product', prod_list, prod_template)

cour_handler = CSVFile('data/courier_list.csv')
cour_list = cour_handler.load()
cour_template = CSVFile('data/courier_template.csv').load()[0]
courier_menu = CSVListMenu('courier', cour_list, cour_template)

order_handler = CSVFile('data/order_list.csv')
order_list = order_handler.load()
order_template = CSVFile('data/order_template.csv').load()[0]
ord_menu = CSVListMenu('order', order_list, order_template)

handler_list = [
    prod_handler, 
    cour_handler, 
    order_handler,
    ]

all_list = [
    prod_list, 
    cour_list, 
    order_list,
    ]

def save(handler: MyFileHandler, input_list: list):
    return handler.save(input_list)

def save_all():
    return all(map(save, handler_list, all_list))

def print_main_menu():
    print(
        "1. Products Menu\n" 
        "2. Courier Menu\n" 
        "3. Orders Menu\n" 
        "0. Exit"
    )

def main_menu_choice() -> bool:
    user_input = get_input("Please enter a number to select your menu choice: ",'int')
    print_buffer()
    match user_input:
        case 1:
            prod_menu.start()
        case 2:
            courier_menu.start()
        case 3:
            ord_menu.start()
        case 0:
            save_all()
            return False
        case _:
            print("Please select a valid option\n")
    return True

@menu_loop
def main():
    print_main_menu()
    return main_menu_choice()

# IF user input is 0: EXIT app

if __name__ == "__main__":
    print_buffer()
    print("Welcome to York's Fromage Frenzy")
    print_buffer()
    main()
