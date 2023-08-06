__date__ = "11.03.2021"
__status__ = "Development"
__annotations__ = "Enthält die Exceptions für Passworte"
__doc__ = """
Passwort Exceptions:

PasswordError:
    ist die Klasse, von der die anderen Passwort-Exceptions erben.

WrongPassword:
    ist die Exception, falls ein falsches Passwort verwendet wurde.
"""


class PasswordError(Exception):
    CODE = "PasswordError"

    def __init__(self, msg):
        self.__message = "Es gab einen Fehler beim verwendeten Passwort"
        super(PasswordError, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass


class WrongPassword(PasswordError):
    CODE = "WrongPassword"

    def __init__(self, file: str = None):
        self.__message = f"Der verwendete Schlüssel {f'für {file} ' if file else ''}ist nicht richtig"
        super(WrongPassword, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass
