__date__ = "11.03.2021"
__status__ = "Development"
__annotations__ = "Enthält die Exceptions für das Verschlüsseln und Entschlüsseln von Texten"
__doc__ = """
Text Exceptions:

TextError:
    ist die Klasse, von der die anderen Text Exceptions erben.

TextIsEncrypted:
    wird ausgelöst, wenn der Text nicht verschlüsselt werden kann, weil er das bereits wurde.

TextIsNotEncrypted:
    wird ausgelöst, wenn Text entschlüsselt werden soll, der gar nicht verschlüsselt worden ist.  
"""


class TextError(Exception):
    CODE = "TextError"

    def __init__(self, msg):
        self.__message = "Es gab einen Fehler beim verwendeten Text"
        super(TextError, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass


class TextIsEncrypted(TextError):
    CODE = "TextIsEncrypted"

    def __init__(self):
        self.__message = "Der verwendete Text kann nicht verschlüsselt werden, da er bereits verschlüsselt wurde."
        super(TextIsEncrypted, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass


class TextIsNotEncrypted(TextError):
    CODE = "TextIsNotEncrypted"

    def __init__(self):
        self.__message = "Der Text kann nich entschlüsselt werden, da er nicht verschlüsselt wurde."
        super(TextIsNotEncrypted, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass
