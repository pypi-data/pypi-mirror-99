from .print_manager import mcprint
from .input_validation import get_input
from .utilities import clear
import logging


class MenuFunction:
    """Allows to assign a user defined function to the Menu

    If the function requires arguments, these can be defined while creating
    a MenuFunction. This MenuFunction must be placed inside the options argument in Menu

    Args:
        title (str): Name to display on the Menu
        function (function): Function to be called once it is selected on the Menu

    Example:
        The following example showcases how to define a new ``MenuFunction``
        using a user defined function which requires arguments

        >>> import mcutils as mc
        ...
        >>> def foo(n):
        ...     return n**2
        ...
        >>> mf_foo = mc.MenuFunction(title='do foo',
        ...                          function=foo,
        ...                          n=4)

        The example above, defines a ``MenuFunction`` which has attached
        a user defined function ``foo(n)``

    """
    def __init__(self, title=None, function=None, **kwargs):
        self.function = function
        self.title = title
        self.kwargs = kwargs
        self.returned_value = None

    def print_function_info(self):
        mcprint('Function: %s' % self.function)

        for parameter in self.kwargs:
            mcprint(parameter)

    def get_unassigned_params(self):
        unassigned_parameters_list = []
        for parameter in self.function.func_code.co_varnames:
            if parameter not in self.kwargs:
                mcprint(parameter)
                unassigned_parameters_list.append(parameter)
        return unassigned_parameters_list

    def get_args(self):
        mcprint(self.kwargs)
        return self.kwargs

    def call_function(self):
        self.returned_value = self.function(**self.kwargs)
        return self.returned_value


class Menu:
    """Main structure for generating menus

    Args:
        title (str): Title of the menu
        subtitle (str): Subtitle of the menu
        text (str): Text of the menu
        options (list): list or dict of the available options to select from
        return_type (type): Indicates the required return type
        parent (Menu): The parent of the current menu. Used to head back to the previous menu
        input_each (bool): If true, the menu will ask the user to input the value for each of the options. Returns a dict
        back (bool): If true and adittional option with index 0 will appear in the menu. Use this to head back to the previous Menu.

    Attributes:
        return_value (object): If input_each = False, returns the selected index of the Menu. If input_each = True
                            returns a dictionary containing the options as keys and the values introduced by the user
        function_returned_value (object): Returns the returned by the user defined function from MenuFunction

    Example:
        Create simple Menu

        >>> import mcutils as mc
        >>> mc_menu = mc.Menu(title='Main Menu',
        ...                   subtitle='Subtitle',
        ...                   text='Please select one of the following options',
        ...                   options=['Option 1', 'Option 2', 'Option 3'])
        >>> mc_menu.show()
        ...
        === Main Menu
        - - Subtitle
        ...
        Please select one of the following options
        1. Option 1
        2. Option 2
        3. Option 3
        0. Back
        >>


    Example:
        Create Menu using user defined functions and submenus

        The following example explains how to display other menus as
        submenus, and call user defined functions
        >>> import mcutils as mc
        >>> def foo(n):
        ...     return n**2
        ...
        >>> mf_foo = mc.MenuFunction(title='do foo', function=foo, n=4)
        ...
        >>> mc_submenu = mc.Menu(title='Submenu',
        ...                      text='This is the submenu',
        ...                      options=[mf_foo])
        ...
        >>> mc_menu = mc.Menu(title='Main Menu',
        ...                   subtitle='Subtitle',
        ...                   text='Please select one of the following options',
        ...                   options=[mc_submenu, 'Option 2', 'Option 3'])
        ...
        >>> mc_menu.show()
        >>> print(mc_submenu.function_returned_value)

        As shown above, two menus were defined. One for the main menu ``mc_menu``,
        and the one for the submenu ``mc_submenu``. A user defined function was defined aswell
        as ``mf_foo``. The submenu was added into the options of main menu, while the user defined
        function was assigned to the submenu.

    """
    def __init__(self, title: str = None, subtitle: str = None, text: str = None,
                 options=None, return_type: type = int, parent=None,
                 input_each: bool = False,
                 previous_menu=None, back: bool = True):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.options = options
        self.return_type = return_type
        self.parent = parent
        self.input_each = input_each
        self.previous_menu = previous_menu
        self.back = back
        self.returned_value = None
        self.function_returned_value = None

    def set_parent(self, parent):
        self.parent = parent

    def set_previous_menu(self, previous_menu):
        self.previous_menu = previous_menu

    def get_selection(self):

        start_index = 1
        if self.back:
            start_index = 0

        # if there exist options it means user have to select one of them
        if (self.options.__len__() != 0) and (not self.input_each):

            while True:

                selection = get_input()

                if selection.__str__().isdigit():
                    if int(selection) in range(start_index, (self.options.__len__()) + 1):
                        if int(selection) != 0:
                            if isinstance(self.options[int(selection) - 1], MenuFunction):
                                function = self.options[int(selection) - 1]
                                self.function_returned_value = function.call_function()
                            elif isinstance(self.options[int(selection) - 1], Menu):
                                sub_menu = self.options[int(selection) - 1]
                                sub_menu.set_parent(self)
                                sub_menu.show()
                        else:
                            if self.parent:
                                self.parent.set_previous_menu(self)
                                self.parent.show()
                        break
                    else:
                        logging.warning('Index not in range')

                else:
                    logging.warning('Entered value must be int')

        elif self.input_each:
            selection = {}
            for option in self.options:
                if isinstance(self.options, dict):
                    filter_criteria = self.options[option]
                    return_type = int
                    if filter_criteria[0] in [str, int]:
                        return_type = filter_criteria[0]
                        filter_criteria = filter_criteria[1:]
                    parameter_value = get_input(format_='{} >> '.format(option),
                                                valid_options=filter_criteria,
                                                return_type=return_type)
                else:
                    parameter_value = get_input('{} >> '.format(option))
                selection[option] = parameter_value

        # if there aren't any option it means user must input a string
        else:
            selection = get_input()

        self.returned_value = selection
        return selection

    def show(self):
        """Display the menu once

        The Menu will be displayed until the required operations are completed"""
        # if(self.previous_menu != None) and (self != self.previous_menu):
        #     del(self.previous_menu)
        clear()
        if self.title:
            mcprint('=== %s ' % self.title)
        if self.subtitle:
            mcprint('- - %s' % self.subtitle)
        print()
        if self.text:
            mcprint(self.text)

        # print 'Parent:',self.parent
        if self.options and not self.input_each:
            for index, option in enumerate(self.options):
                if isinstance(option, MenuFunction):
                    print('%s. %s' % (str(index + 1), option.title))
                elif isinstance(option, Menu):
                    print('%s. %s' % (str(index + 1), option.title))
                else:
                    print('%s. %s' % (str(index + 1), option))
            if self.back:
                mcprint('0. Back')

        selected_option = self.get_selection()
        return selected_option

