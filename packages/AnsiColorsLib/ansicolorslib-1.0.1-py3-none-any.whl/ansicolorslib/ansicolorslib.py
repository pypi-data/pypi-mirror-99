#!/usr/bin/python3
import random

def ansirgb(red: int, green: int, blue: int) -> str:
    """
    This function converts RGB values to ANSI color codes.
    
    @param red: Red value of RGB 0-255.
    @type red: int.
    @param green: Green value of RGB 0-255.
    @type green: int.
    @param blue: Blue value of RGB 0-255.
    @type blue: int.

    @return: ANSI color code string.
    @rtype str.
    """
    
    return "\033[38;2;{};{};{}m".format(red, green, blue)


def validate_parameter(param: tuple, strlen: int) -> bool: 
    if len(param) != 3:
        return False
    type_bool: bool = all((type(param[0]) == int, type(param[1]) == int, type(param[2]) == str))
    size_bool: bool = all((param[0] >= 0, param[1] > 0, param[0] < param[1], param[1] <= strlen))
    return type_bool and size_bool


class Colors:
    ENDC = "\033[0m"  # Clear all ANSI changes.
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    HEADER = BOLD + UNDERLINE

    RED = ansirgb(255, 0, 0)
    GREEN = ansirgb(0, 255, 0)
    ORANGE = ansirgb(255, 128, 0)
    BLUE = ansirgb(0, 128, 255)
    LIGHT_BLUE = ansirgb(51, 153, 255)
    LIGHT_GREEN = ansirgb(0, 255, 128)
    PURPLE = ansirgb(128, 0, 255)
    CYAN = ansirgb(0, 255, 255)
    TURQUOISE = ansirgb(64, 224, 208)
    WHITE = ansirgb(255, 255, 255)
    BLACK = ansirgb(0, 0, 0)
    YELLOW = ansirgb(255, 255, 0)
    PINK = ansirgb(255, 0, 255)

    BOLD_RED = RED + BOLD
    BOLD_GREEN = GREEN + BOLD
    BOLD_ORANGE = ORANGE + BOLD
    BOLD_BLUE = BLUE + BOLD
    BOLD_LIGHT_GREEN = LIGHT_GREEN + BOLD
    BOLD_PURPLE = PURPLE + BOLD
    BOLD_CYAN = CYAN + BOLD
    BOLD_TURQUOISE = TURQUOISE + BOLD
    BOLD_WHITE = WHITE + BOLD
    BOLD_BLACK = BLACK + BOLD
    BOLD_YELLOW = YELLOW + BOLD
    BOLD_PINK = PINK + BOLD
    
    @staticmethod
    def ansirgb(red: int, green: int, blue: int) -> str:
        """
        This function converts RGB values to ANSI color codes.
    
        @param red: Red value of RGB 0-255.
        @type red: int.
        @param green: Green value of RGB 0-255.
        @type green: int.
        @param blue: Blue value of RGB 0-255.
        @type blue: int.

        @return: ANSI color code string.
        @rtype str.
        """
        return ansirgb(red, green, blue)


    @staticmethod
    def rand_color() -> str:
        """
        This function returns a random ANSI color code string.

        @return: Random ANSI color value string.
        @rtype str.
        """
        return rgb(
            random.choice(range(255)),
            random.choice(range(255)),
            random.choice(range(255)))


    @staticmethod
    def print_success(success: str = "SUCCESS!", begins_with: str = "", ends_with: str = "") -> None:
        """
        This function prints a given success message.

        @param success: The specified success message.
        @type success: str.
        @param begins_with: Optional string to start with.
        @type starts_with: str.
        @param ends_with: Optional string to end with.
        @type ends_with: str.

        @return: None.
        """
        print(
            begins_with
            + Colors.ENDC
            + "["
            + Colors.BOLD_GREEN
            + "!"
            + Colors.ENDC
            + "] "
            + Colors.BOLD_GREEN
            + success
            + Colors.ENDC
            + ends_with)
    

    @staticmethod
    def print_information(info: str, begins_with: str = "", ends_with: str = "") -> None:
        """
        This function prints a given information message.

        @param info: The specified information message.
        @type info: str.
        @param begins_with: Optional string to start with.
        @type starts_with: str.
        @param ends_with: Optional string to end with.
        @type ends_with: str.

        @return: None.
        """
        print(
            begins_with
            + Colors.ENDC
            + "["
            + Colors.LIGHT_BLUE
            + "?"
            + Colors.ENDC
            + "] "
            + Colors.LIGHT_BLUE
            + info
            + Colors.ENDC
            + ends_with)
    

    @staticmethod
    def print_warning(warning: str = "WARNING!", begins_with: str = "", ends_with: str = "") -> None:
        """
        This function prints a specified warning message.

        @param warning: The specified warning.
        @type warning: str.
        @param begins_with: Optional string to start with.
        @type starts_with: str.
        @param ends_with: Optional string to end with.
        @type ends_with: str.

        @return: None.
        """
        print(
            begins_with
            + Colors.ENDC
            + "["
            + Colors.BOLD_YELLOW
            + "!"
            + Colors.ENDC
            + "] "
            + Colors.BOLD_YELLOW
            + warning
            + Colors.ENDC
            + ends_with)


    @staticmethod
    def print_error(error: str = "ERROR!", begins_with: str = "", ends_with: str = "") -> None:
        """
        This function prints a specified error message.

        @param error: The specified error.
        @type error: str
        @param begins_with: Optional string to start with.
        @type starts_with: str.
        @param ends_with: Optional string to end with.
        @type ends_with: str.

        @return: None.
        """
        print(
            begins_with
            + Colors.ENDC
            + "["
            + Colors.BOLD_RED
            + "!"
            + Colors.ENDC
            + "] "
            + Colors.BOLD_RED
            + error
            + Colors.ENDC
            + ends_with)


    @staticmethod
    def ansiprint(text: str, ansi_mod: str = "", begins_with: str = "", ends_with: str = "") -> None:
        """
        This function is meant to replace the default python print function, it adds the ability to print text in colors.

        @param text: The text to print with modifications.
        @type text: str.
        @param ansi_mod: The modifications we want to apply to the text. Defaults to "".
        @type ansi_mod: str, optional.
        @param begins_with: An optional string to begin with, does not get affected by the ansi modifications. Defaults to "".
        @type begins_with: str, optional.
        @param ends_with: An optional string to end with, does not get affected by the ansi modifications. Defaults to "".
        @type ends_with: str, optional.

        @return: None.
        """
        print(begins_with + ansi_mod + text + Colors.ENDC + ends_with)

    @staticmethod
    def modify_string(input_str: str, parameters: list) -> str:
        """
        This function receives a string to modify and the parameters to modify it with.
        Each parameter is a tuple 3 values long, the first two are start and stop indexes for the wanted modification.
        ? Important: Please make sure that you send a *LIST* of tuples and not a single tuple.
        ? Important Note: We strongly advise you to use the included ANSI modifications given in this class.
        ! PLEASE NOTE: You cannot specify colliding indexes!
        !   For example: 
        !       (0, 5) and (2, 10) will not work correctly! if you wish to combine several modifications you can do so by specifying them like so:
                    > COLOR_MANAGER.modify_string("abcdefg", [(0, 4, COLOR_MANAGER.GREEN + COLOR_MANAGER.BOLD)])
                    > This will result in a bold green `abcd` and the rest as normal text.
        ! PLEASE NOTE: the start and stop indexes are not direct indexes but are used like the string indices in python,
        !   Which means that the stop index is not included in the final string.
        !   For example:
        !       in the string "hello, world!", to modify the word `hello` we will use the indexes (0, 5).
        
        @param input_str: The string to modify with the given parameters.
        @type input_str: str.
        @param parameters: The parameters to modify the string with, each parameter is a tuple of:
        >   (begin_index : int, stop_index : int, ansi_modification : str).
        @type parameters: list[tuple].
        @return: The modified string with the valid changes made to it, if for some reason there are some missing changes please read the description.
        @rtype str.
        """
        # Get list of all valid parameters.
        valid_params = [param for param in parameters if validate_parameter(param, len(input_str))]
        if len(valid_params) == 0:
            return input_str
        
        # Get lists of all the needed indexes and sort them from last to first.
        endc_indexes = list(set([param[1] for param in valid_params]))
        endc_indexes.sort(reverse=True)
        mod_indexes = list(set([(param[0], param[2]) for param in valid_params]))
        mod_indexes.sort(key=lambda x: x[0], reverse=True)
        
        output_str = Colors.ENDC
        ansi_to_add = ""

        prev_index = len(input_str)
        index = 0
        skip_endc = False

        modi = 0
        endci = 0
        while modi < len(valid_params) or endci < len(valid_params):
            mod_index = None
            endc_index = None
            if modi < len(valid_params):
                mod_index = mod_indexes[modi] # Current modification parameter.
            if endci < len(valid_params):
                endc_index = endc_indexes[endci] # Current endc parameter.
            
            if mod_index is not None and endc_index is not None:
                # Check which one should go before the other.
                if mod_index[0] > endc_index:
                    index = mod_index[0]
                    ansi_to_add = mod_index[1]
                    modi += 1
                elif mod_index[0] < endc_index:
                    if not skip_endc:
                        index = endc_index
                        ansi_to_add = Colors.ENDC
                        endci += 1
                    skip_endc = False
                else:
                    # Both need to be used and therefor we must put the endc first so the color will continue.
                    index = endc_index
                    ansi_to_add = Colors.ENDC + mod_index[1]
                    skip_endc = True
                    modi += 1
                    endci += 1
            elif mod_index is not None:
                index = mod_index[0]
                ansi_to_add = mod_index[1]
                modi += 1
            elif endc_index is not None:
                index = endc_index
                ansi_to_add = Colors.ENDC
                endci += 1
            
            # Append the modified text to the output string.
            output_str = ansi_to_add + input_str[index: prev_index] + output_str
            prev_index = index
        
        if index != 0:
            # If we did not reach the beginning of the string we need to add it.
            output_str = input_str[0: prev_index] + output_str
        
        return output_str


COLOR_MANAGER = Colors()  # Colors Object.