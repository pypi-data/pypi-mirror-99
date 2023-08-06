from AESEncryptor_heureka_code.Exceptions import WrongPassword, PasswordError, FileIsEncrypted, FileIsNotEncrypted, FileError, \
    TextError, TextIsEncrypted, TextIsNotEncrypted

from AESEncryptor_heureka_code.AESFileEncryptor import AESFileEncryptor
from AESEncryptor_heureka_code.AESTextEncryptor import AESTextEncryptor
from AESEncryptor_heureka_code import Exceptions

from AESEncryptor_heureka_code.Exceptions import __doc__ as AESExceptions__doc__
from AESEncryptor_heureka_code.AESFileEncryptor import __doc__ as AESFileEncryptor__doc__
from AESEncryptor_heureka_code.AESTextEncryptor import __doc__ as AESTextEncryptor__doc__

__doc__ = "AES-Encryptor:\n" + f"\n{'-'*100}\n".join([AESFileEncryptor__doc__, AESTextEncryptor__doc__,
                                                      AESExceptions__doc__])
__date__ = "12.03.2021"
__annotations__ = "Enthält die Klassen für den AES-Encryptor und dazugrhöriges"
__status__ = "Development"
__version__ = "1.0.0"
