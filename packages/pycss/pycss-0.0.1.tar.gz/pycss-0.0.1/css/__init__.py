import os

# Errors
class ColourNotFound(ValueError):
    pass

# Basic colors
BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
NOCOLOR = "\u001b[0m"

# Bright colors
C_BLACK = "\u001b[30;1m"
C_RED = "\u001b[31;1m"
C_GREEN = "\u001b[32;1m"
C_YELLOW = "\u001b[33;1m"
C_BLUE = "\u001b[34;1m"
C_MAGENTA = "\u001b[35;1m"
C_CYAN = "\u001b[36;1m"
C_WHITE = "\u001b[37;1m"

# Basic background colors
BGBLACK = "\u001b[40m"
BGRED = "\u001b[41m"
BGGREEN = "\u001b[42m"
BGYELLOW = "\u001b[43m"
BGBLUE = "\u001b[44m"
MGMAGENTA = "\u001b[45m"
BGCYAN = "\u001b[46m"
BGWHITE = "\u001b[47m"

# Bright background colors
C_BGBLACK = "\u001b[40;1m"
C_BGRED = "\u001b[41;1m"
C_BGGREEN = "\u001b[42;1m"
C_BGYELLOW = "\u001b[43;1m"
C_BGBLUE = "\u001b[44;1m"
C_MGMAGENTA = "\u001b[45;1m"
C_BGCYAN = "\u001b[46;1m"
C_BGWHITE = "\u001b[47;1m"

def color(text, color):
    """
    This function will make your text colorful
    :param text: String
    :param color: pycss color
    :return: Colored text
    """

    os.system("cls")

    color_list = [BLACK, RED, GREEN, YELLOW, CYAN, WHITE, BLUE, C_BLACK, C_RED, C_GREEN, C_YELLOW, C_CYAN, C_WHITE, C_BLUE]
    if color not in color_list:
        raise ColourNotFound("The color you passed is not valid")
    else:
        return f"{color}{text}{NOCOLOR}"

def bgcolor(text, background_color):
    """
    This function will apply a background color on your text
    :param text: String
    :param background_color: pycss background color
    :return: Background color on the text
    """
    color_list = [BGBLACK, BGRED, BGGREEN, BGYELLOW, BGCYAN, BGWHITE, BGBLUE, C_BGBLACK, C_BGRED, C_BGGREEN, C_BGYELLOW, C_BGCYAN, C_BGWHITE, C_BGBLUE]

    os.system("cls")

    if background_color not in color_list:
        raise ColourNotFound("The color you passed is not valid")
    else:
        return f"{background_color}{text}{NOCOLOR}"

def bold(text):
    """
    This function will make your text bold
    :param text: String
    :return: Bold text
    """

    os.system("cls")

    return f"\u001b[1m{text}{NOCOLOR}"

def underline(text):
    """
    This function will make your text underlined
    :param text: String
    :return: Underlined text
    """

    os.system("cls")

    return f"\u001b[4m{text}{NOCOLOR}"