import colorama


class ColorSettings:
    """Settings for color printing

    Attributes:
        is_dev (bool): If developing on IDE, this must be True, otherwise False.
        print_color (bool): For printing colors making use of mcutils print_color must be set to True
    """

    is_dev = False
    print_color = True


class Color:
    """All available colors defined by mcutils"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    LIGHTRED = '\033[91m'
    LIGHTGREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHTBLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHTCYAN = '\033[96m'
    RESET = '\033[0m'


def mcprint(text='', format_='', color=None, end='\n'):
    """print to stdout making use of color formatting options

    Args:
        text (str): Text to be displayed on stdout
        format_ (str): Will add this string at the beginning of the text
        color (Color): Color used for displaying the text
        end (str): Overwrites end arguments of the print() statement
    """
    if not ColorSettings.is_dev:
        colorama.init(convert=True)

    text = '{}{}'.format(format_, text)
    if color and ColorSettings.print_color:
        text = "{}{}{}".format(color, text, Color.RESET)
    print(text, end=end)


def enable_color():
    ColorSettings.print_color = True
    colorama.init()


def disable_color():
    ColorSettings.print_color = False
    colorama.deinit()
