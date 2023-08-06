from os.path import getsize, isfile
from os import remove

from base64 import b64decode, b64encode

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from AESEncryptor_heureka_code.Exceptions import WrongPassword, FileIsEncrypted, FileIsNotEncrypted

__author__ = "heureka42"
__date__ = "11.03.2021"
__maintainer__ = "heureka42"
__status__ = "Prototype"
__doc__ = """
class AESFileEncryptor:
    // __init__
    // Nimmt die Argumente:
    //   * passwort: str, das Passwort mit dem Datein verschlüsselt werden sollen.
    //   * signaturtext: str, ist der Text, an dem das Tool eine verschlüsselte Datei erkennt.
    //   * chunks: int, bezeichnet die Blockgröße
    def __init__(self, passwort: str, signaturtext: str = "Gewidmet Lou", chunks: int = 32*1024)
    
    // encrypt
    // Nimmt die Argumente
    //   * file: str, die Datei, die verschlüsselt werden soll.
    //   * delete_orig_after: bool, gibt an, ob die Datei, die verschlüsselt wurde, gelöscht werden soll.
    // Und verschlüsselt eine Datei mit den im Konstruktor festgelegten Parametern
    def encrypt(self, file: str, delete_orig_after: bool = False)
    
    // decrypt
    // Nimmt die Argumente
    //   * file: str, die Datei, die entschlüsselt werden soll.
    //   * delete_orig_after: bool, gibt an, ob die Datei, die entschlüsselt wurde, gelöscht werden soll.
    // Und entschlüsselt eine Datei mit den im Konstruktor festgelegten Parametern
    def decrypt(self, file: str, delete_orig_after: bool = False)
    
    // Gibt den Ausgabestring zurück
    def __str__(self) -> str
    
    // Gibt den Representationsstring aus
    def __repr__(self) -> str
    
    // Gibt die Gleichheit des Arguments mit dem Passwort zurück
    def __eq__(self) -> bool
    
    // Gibt die Ungleichheit des Arguments mit dem Passwort zurück
    def __ne__(self) -> bool
    
    // Gibt die Länge des Passworts zurück
    def __len__(self) -> int
    
    // Sonst nur private Methoden
"""


class AESFileEncryptor:
    def __init__(self, passwort: str, signaturtext: str = "Gewidmet Lou", chunks: int = 32*1024):
        """Initialisiert das Objekt"""
        self.__signaturtext = signaturtext
        self.__chunks = chunks
        self.__passwort = passwort
        pass

    def encrypt(self, file: str, delete_orig_after: bool = False):
        """Verschlüsselt eine Datei"""
        self.__encrypt(file, file + ".enc", delete_orig_after)
        pass

    def decrypt(self, file: str, delete_orig_after: bool = False):
        """Entschlüsselt eine Datei"""
        self.__decrypt(file, delete_orig_after)
        pass

    def __str__(self):
        """Gibt den Ausgabestring des Objekts zurück"""
        return f"<AESFileEncryptor passwort={self.__passwort} " \
               f"signatur={self.__signaturtext}, chunks={self.__chunks}>"

    def __repr__(self):
        """Gibt den Representationsstring zurück"""
        return f"AESFileEncrytor(\"{self.__passwort}\", \"{self.__signaturtext}\", \"{self.__chunks}\")"

    def __eq__(self, other):
        """Gibt zurück, ob das Passwort mit dem des Arguments übereinstimmt"""
        if type(other) == str:
            return self.__passwort == other
        elif type(other) == type(self):
            return self.__passwort == other.__passwort
        pass

    def __ne__(self, other):
        """Gibt zurück, ob das Passwort von dem des Arguments verschieden ist"""
        return self.__eq__(other) is False

    def __len__(self):
        """Gibt die Länge des Passworts zurück"""
        return len(self.__passwort)

    def __get_key_from_password(self) -> bytes:
        return SHA256.new(bytes(self.__passwort, encoding="utf8")).digest()

    def __is_encrypted(self, file):
        with open(file, "rb") as f_input:
            return self.__signaturtext == str(f_input.read(len(self.__signaturtext)), encoding="utf8")
        pass

    def __get_file_key(self, file):
        with open(file, "rb") as f_in:
            signatur = f_in.read(len(self.__signaturtext))
            key = f_in.read(32)
        return key

    def __datei_existiert_pruefung(self, file):
        if isfile(file):
            pass
        else:
            raise FileNotFoundError
        pass

    def __datei_bereits_verschluesselt_pruefung(self, file):
        if self.__is_encrypted(file):
            raise FileIsEncrypted
        pass

    def __datei_nicht_verschluesselt_pruefung(self, file):
        if self.__is_encrypted(file):
            pass
        else:
            raise FileIsNotEncrypted
        pass

    def __datei_kann_mit_passwort_entschlusselt_werden(self, file):
        if self.__get_file_key(file) != SHA256.new(self.__get_key_from_password()).digest():
            raise WrongPassword
        pass

    def __encrypt(self, file: str, out_file_name, delete_orig_after=False):
        self.__datei_existiert_pruefung(file)
        self.__datei_bereits_verschluesselt_pruefung(file)

        filesize = str(getsize(file)).zfill(16)
        IV = Random.new().read(16)
        encrytor = AES.new(self.__get_key_from_password(), AES.MODE_CFB, IV)

        with open(file, "rb") as f_input:
            with open(out_file_name, "wb") as f_output:
                f_output.write(bytes(self.__signaturtext, encoding="utf8"))
                f_output.write(SHA256.new(self.__get_key_from_password()).digest())
                f_output.write(filesize.encode("utf-8"))
                f_output.write(IV)
                while True:
                    chunk = f_input.read(self.__chunks)
                    if len(chunk) == 0:
                        break
                    if len(chunk) % 16 != 0:
                        chunk += b" " * (16 - (len(chunk) % 16))
                    f_output.write(encrytor.encrypt(chunk))
                pass
            pass
        if delete_orig_after:
            remove(file)
        pass

    def __decrypt(self, file: str, delete_orig_after=False):
        self.__datei_nicht_verschluesselt_pruefung(file)
        self.__datei_kann_mit_passwort_entschlusselt_werden(file)

        out_file_name = file.rstrip(".enc")
        with open(file, "rb") as f_input:
            self.__datei_nicht_verschluesselt_pruefung(file)
            header_signatur = f_input.read(len(self.__signaturtext))
            key_hash = f_input.read(32)
            filesize = int(f_input.read(16))
            IV = f_input.read(16)
            decryptor = AES.new(self.__get_key_from_password(), AES.MODE_CFB, IV)
            with open(out_file_name, "wb") as f_output:
                while True:
                    chunk = f_input.read(self.__chunks)
                    if len(chunk) == 0:
                        break
                    f_output.write(decryptor.decrypt(chunk))
                f_output.truncate(filesize)
                pass
            pass
        if delete_orig_after:
            remove(file)
        pass
    pass
