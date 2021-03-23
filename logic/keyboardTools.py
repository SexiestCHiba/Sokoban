import typing


class KeyboardTools:
    @classmethod
    def check_integer_keyboard(cls, key: str):
        """Return the integer value of a keyboard key or none if the kay has no integer value"""
        try:
            return int(key[-1])
        except ValueError:
            return None
        except IndexError:
            return None

    @classmethod
    def get_str_from_keyboard_event(cls, key):
        """Return the key value as a string, if the key value is a number, the number is converted into a 
        string before being returned"""
        number = cls.check_integer_keyboard(key)
        key_name = key.split("_")[1]
        if number is None:
            return key_name
        else:
            return str(number)

    @classmethod
    def get_keys_event_from_choices(cls, choices: typing.List[str]):
        """Raise an error if the list 'choices' is not full of string types objects. This function
        also get all the caracthers in the list lower (no capital letters are returned). Then it return the list """

        choices = choices[:]
        i = 0
        while i < len(choices):
            if isinstance(choices[i], str):
                if len(choices[i]) == 1:
                    choices[i] = "K_" + choices[i].lower()
                else:
                    choices[i] = "K_" + choices[i].upper()
            else:
                raise ValueError("The choices must be a list of str.")
            i += 1

        return choices

    @classmethod
    def get_keys_event_from_range(cls, start: int, end: int):
        """Create a keys list with a length higher than the 'start' variable and lower than 
        the 'end' variable"""
        if not 0 <= start <= end <= 9:
            raise ValueError(
                "start and end have to respect : 0 <= start <= end <= 9.")

        keys = []
        for i in range(start, end + 1):
            keys.append("K_KP" + str(i))
            keys.append("K_" + str(i))

        return keys
