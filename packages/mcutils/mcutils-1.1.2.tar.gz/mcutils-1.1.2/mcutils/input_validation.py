from .print_manager import mcprint, Color
import logging


def exit_application(text: str = None, enter_quit: bool =False):
    """Exit application

    Args:
        text (str): Text to display before exiting
        enter_quit (bool): If true, user must press enter before exiting
    """
    if text:
        mcprint(text=text, color=Color.YELLOW)
    logging.info('Exiting Application Code:0')
    if enter_quit:
        get_input('Press Enter to exit...')
    exit(0)


def print_error(operators_list=None, contains_list=None, return_type=None):
    if operators_list:
        for operator in operators_list:
            if return_type == int:
                logging.warning('input must be {}'.format(operator))
            elif return_type == str:
                logging.warning('input length must be {}'.format(operator))
    if contains_list:
        logging.warning('input must be one of the following')
        for contains in contains_list:
            mcprint(text='\t{}'.format(contains), color=Color.RED)


def input_validation(user_input, return_type, valid_options):
    if return_type == int:
        if not user_input.isnumeric():
            return False
        user_input = int(user_input)

    # Contains validation
    if valid_options:

        operators_list = list(filter(lambda x: str(x).startswith(('<', '>', '==', '!=')), valid_options))
        contains_list = list(set(valid_options) - set(operators_list))

        # Complex validation
        # Special operators
        for operator in operators_list:
            if '<=' in operator:
                value = operator.replace('<=', '')
                if return_type == int:
                    if not user_input <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>=' in operator:
                value = operator.replace('>=', '')
                if return_type == int:
                    if not user_input >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '<' in operator:
                value = operator.replace('<', '')
                if return_type == int:
                    if not user_input < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>' in operator:
                value = operator.replace('>', '')
                if return_type == int:
                    if not user_input > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '==' in operator:
                value = operator.replace('==', '')
                if return_type == int:
                    if not user_input == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
            elif '!=' in operator:
                value = operator.replace('!=', '')
                if return_type == int:
                    if not user_input != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

        # if contains in valid options
        if len(contains_list) > 0:
            if user_input not in contains_list:
                return False

    return True


def get_input(format_: str = '>> ', text: str = None, can_exit: bool = True, exit_input: str= 'exit',
              valid_options: list = None, return_type: type = str,
              validation_function=None, color: Color = None):
    """
    Require the user to input a value

    Args:
        format_ (str): Will add this string at the beginning of the text
        text (str): Text to be displayed before input
        can_exit (bool): If true, when user types the exit_input command, the application will exit
        exit_input (str): Special string, when user inputs this command, the application will exit
        valid_options (list): If the input of the user is not in valid_options, the menu will ask for it again
        return_type (type): Indicates the required return type
        validation_function (function): Function used to validate if the input is correct
        color (Color): Color used for displaying the text
    """
    if text:
        mcprint(text=text, color=color)

    while True:
        user_input = input(format_)

        # Emergency exit system
        if user_input == exit_input:
            if can_exit:
                exit_application()
            else:
                logging.warning('Can\'t exit application now')

        # This is the build-in validations system
        if validation_function:
            validation = validation_function.__call__(user_input)

        # This is the external validation system
        else:
            # from input_validation import input_validation
            validation = input_validation(user_input=user_input, return_type=return_type, valid_options=valid_options)
        if validation:
            break

        logging.warning('Not Valid Entry')

    return user_input
