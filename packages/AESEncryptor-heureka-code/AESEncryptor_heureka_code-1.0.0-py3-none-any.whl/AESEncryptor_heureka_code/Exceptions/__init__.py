from .PasswordExceptions import PasswordError, WrongPassword
from .FileExceptions import FileError, FileIsEncrypted, FileIsNotEncrypted
from .TextExceptions import TextError, TextIsEncrypted, TextIsNotEncrypted

from .PasswordExceptions import __doc__ as PasswordExceptions__doc__
from .FileExceptions import __doc__ as FileExceptions__doc__
from .TextExceptions import __doc__ as TextExceptions__doc__

__doc__ = "Exceptions:\n" + f"\n{'-'*100}\n".join([PasswordExceptions__doc__, FileExceptions__doc__,
                                                   TextExceptions__doc__])
__date__ = "11.03.2021"
__annotations__ = "Enthält die Exceptions für den AES-Encryptor"
__status__ = "Development"
