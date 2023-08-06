__date__ = "11.03.2021"
__status__ = "Development"
__annotations__ = "Enthält die Exceptions für Passworte"
__doc__ = """
Datei Exceptions:

FileError:
    ist die Klasse, von der die anderen File-Exceptions erben.

FileIsEncrypted:
    wird ausgelöst, wenn eine Datei reschlüsselt werden soll, die bereits verschlüsselt worden ist.

FileIsNotEncrypted:
    wird ausgelöst, wenn eine Datei entschlüsselt werden soll, die nicht entschlüsselbar ist.
"""


class FileError(Exception):
    CODE = "FileError"

    def __init__(self, file):
        self.__message = f"Bei der Datei {file} ist ein Fehler aufgetreten"
        super(FileError, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass


class FileIsEncrypted(FileError):
    CODE = "FileIsEncrypted"

    def __init__(self, file):
        self.__message = f"Die Datei {file} ist bereits verschlüsselt und kann nicht erneut verschlüsselt werden."
        super().__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass


class FileIsNotEncrypted(FileError):
    CODE = "FileIsNotEncrypted"

    def __init__(self, file):
        self.__message = f"Die Datei {file} kann nicht entschlüsselt werden, da sie nicht (mit diesem Tool) " \
                         f"verschlüsselt oder ein anderer Signaturtext verwendet wurde"
        super(FileIsNotEncrypted, self).__init__(self.__message)
        pass

    def __str__(self):
        return self.__message
    pass
