from colorama import Fore
import sys
from koinput.inputs import int_input


class Menu:

    def __init__(self):
        self.__items = {}

    def add_to_menu(self, name: str, func, *args):
        self.__items[name] = (func, args)

    def add_to_menu_dec(self, name: str, *args):
        def decorator(func):
            self.__items[name] = (func, args)
            return func

        return decorator

    @staticmethod
    def menu_exit(exit_offer: str):
        def f():
            print(exit_offer, end='')
            input()

        return f

    def reassign_menu_exit(self):
        def decorator(func):
            self.menu_exit = func
            return func

        return decorator

    def show_menu(self, title: str = None, title_style: str = None, number_of_leading_spaces_title: int = 2,
                  console_style: str = Fore.RESET, order_of_items: tuple = None, number_of_leading_spaces: int = 4,
                  separator: str = ' - ', items_style: str = None, input_suggestion: str = 'Select a menu item: ',
                  enable_menu_item_exit: bool = True, menu_item_exit: str = 'Exit',
                  exit_offer: str = 'Press Enter to exit...', input_suggestion_style: str = None):

        # Type check
        if type(title) != str and title is not None:
            raise TypeError('title must be str')
        if type(title_style) != str and title_style is not None:
            raise TypeError('title_colour must be str')
        if type(items_style) != str and items_style is not None:
            raise TypeError('items_style must be str')
        if type(input_suggestion_style) != str and input_suggestion_style is not None:
            raise TypeError('input_suggestion_style must be str')
        if type(number_of_leading_spaces) != int:
            raise TypeError('number_of_leading_spaces must be int')
        if type(number_of_leading_spaces_title) != int:
            raise TypeError('number_of_leading_spaces_title must be int')
        if type(console_style) != str:
            raise TypeError('console_colour must be str')
        if type(separator) != str:
            raise TypeError('separator must be str')
        if type(input_suggestion) != str:
            raise TypeError('input_suggestion must be str')
        if type(enable_menu_item_exit) != bool:
            raise TypeError('enable_menu_item_exit must be bool')
        if type(menu_item_exit) != str:
            raise TypeError('menu_item_exit must be str')
        if type(exit_offer) != str:
            raise TypeError('exit_offer must be str')
        if type(order_of_items) != tuple and order_of_items is not None:
            raise TypeError('order_of_items must be a tuple of int or str')

        # order_of_items type check
        order_of_items_is_int_tuple = True
        if order_of_items is not None:
            for item in order_of_items:
                if type(item) != int:
                    order_of_items_is_int_tuple = False
                    for itemstr in order_of_items:
                        if type(itemstr) != str:
                            raise TypeError('order_of_items must be a tuple of int or str')
                        if itemstr not in self.__items:
                            raise IndexError(
                                'order_of_items consisting of str must contain only the names of menu items')
                    break
                if item < 0 or item >= len(self.__items):
                    raise IndexError(
                        'order_of_items consisting of int must contain only '
                        'ordinal numbers of menu items starting from 0')

        if enable_menu_item_exit:
            self.add_to_menu(menu_item_exit, self.menu_exit(exit_offer))

        while True:
            # Title
            if title is not None:
                if title_style is not None:
                    sys.stdout.write(title_style + '\r')
                    sys.stdout.write(' ' * len(title_style) + '\r')
                sys.stdout.write(' ' * number_of_leading_spaces_title + title + console_style + '\n')

            # Menu
            number = 1
            if order_of_items is None:
                for name in list(self.__items.keys()):
                    if items_style is not None:
                        sys.stdout.write(items_style + '\r')
                        sys.stdout.write(' ' * len(items_style) + '\r')
                    sys.stdout.write(' ' * number_of_leading_spaces + f'{number}{separator}{name}{console_style}\n')
                    number += 1
                x = int_input(input_suggestion=input_suggestion, greater=0, less=number,
                              input_suggestion_style=input_suggestion_style)
                if x == number - 1:
                    enable_menu_item_exit = False
                item = self.__items[list(self.__items.keys())[x - 1]]
                if item[0] is not None:
                    item[0](*item[1])

            elif order_of_items_is_int_tuple:
                if enable_menu_item_exit:
                    order_of_items = (*order_of_items, len(self.__items.keys()) - 1)
                for i in order_of_items:
                    if items_style is not None:
                        sys.stdout.write(items_style + '\r')
                        sys.stdout.write(' ' * len(items_style) + '\r')
                    sys.stdout.write(
                        ' ' * number_of_leading_spaces + f'{number}{separator}{list(self.__items.keys())[i]}{console_style}\n')
                    number += 1
                x = int_input(input_suggestion=input_suggestion, greater=0, less=number,
                              input_suggestion_style=input_suggestion_style)
                if x == number - 1:
                    enable_menu_item_exit = False
                item = self.__items[list(self.__items.keys())[order_of_items[x - 1]]]
                if item[0] is not None:
                    item[0](*item[1])

            else:
                if enable_menu_item_exit:
                    order_of_items = (*order_of_items, menu_item_exit)
                for i in order_of_items:
                    if items_style is not None:
                        sys.stdout.write(items_style + '\r')
                        sys.stdout.write(' ' * len(items_style) + '\r')
                    sys.stdout.write(' ' * number_of_leading_spaces + f'{number}{separator}{i}{console_style}\n')
                    number += 1
                x = int_input(input_suggestion=input_suggestion, greater=0, less=number,
                              input_suggestion_style=input_suggestion_style)
                if x == number - 1:
                    enable_menu_item_exit = False
                item = self.__items[order_of_items[x - 1]]
                if item[0] is not None:
                    item[0](*item[1])

            if not enable_menu_item_exit:
                break
