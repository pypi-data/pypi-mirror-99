from base64 import b64decode as __b64decode
from base64 import b64encode as __b64encode

from Crypto import Random as __Random
from Crypto.Cipher import AES as __AES
from Crypto.Hash import SHA256 as __SHA256

from AESEncryptor_heureka_code.Exceptions import WrongPassword, TextIsNotEncrypted, TextIsEncrypted

__author__ = "heureka42"
__date__ = "11.03.2021"
__maintainer__ = "heureka42"
__status__ = "Prototype"
__doc__ = """
class AESTextEncryptor:
    // __init__
    // Nimmt die Argumente:
    //   * passwort, ein String, der das Passwort für die Verschlüsselung ist
    //   * signaturtext, ein String, an dem das Programm einen verschlüsselten Text erkennt
    //   * chunks, bezeichnet die Blockgröße
    def __init__(self, passwort: str, signaturtext: str = "Gewidmet Lou", chunks: int = 32*1024)
    
    // encrypt
    // Nimmt das Argument:
    //   * text, der String, der verschlüsselt werden soll.
    // Liefert einen String im base64 Format zurück
    def encrypt(self, text: str) -> str
    
    // decrypt
    // Nimmt das Argument:
    //   * text, ein String im base64 Format, der entschlüsselt werden soll.
    // Liefert einen String mit dem entschlüsselten Text zurück
    def decrypt(self, text: str) -> str
    
    // Gibt den Ausgabestring zurück
    def __str__(self) -> str
    
    // Gibt den Representationsstring zurück
    def __repr__(self) -> str
    
    // Gibt zurück, ob das Passwort mit dem des Arguments übereinstimmt
    def __eq__(self, other) -> bool
    
    // Gibt zurück, ob das Passwort dem Argument ungleich ist
    def __ne__(self, other) -> bool
    
    // Gibt die Länge des Passworts zurück
    def __len__(self) -> int
    
    // Und private Methoden
"""


class AESTextEncryptor:
    def __init__(self, passwort: str, signaturtext: str = "Gewidmet Lou", chunks: int = 32 * 1024):
        self.__signaturtext = signaturtext
        self.__chunks = chunks
        self.__passwort = passwort
        pass

    def encrypt(self, text: str) -> str:
        self.__text_bereits_verschluesselt_pruefung(text)

        out_bytes = bytes()
        size = str(len(text)).zfill(16)
        IV = __Random.new().read(16)
        encrytor = __AES.new(self.__get_key_from_password(), __AES.MODE_CFB, IV)

        out_bytes += bytes(self.__signaturtext, encoding="utf8")
        out_bytes += __SHA256.new(self.__get_key_from_password()).digest()
        out_bytes += size.encode("utf-8")
        out_bytes += IV
        index = 0
        while True:
            chunk = bytes(text[index: index+self.__chunks], encoding="utf8")
            if len(chunk) == 0:
                break
            if len(chunk) % 16 != 0:
                chunk += b" " * (16 - (len(chunk) % 16))
            out_bytes += encrytor.encrypt(chunk)
            index += self.__chunks
        return str(__b64encode(out_bytes), encoding="utf8")

    def decrypt(self, text: str) -> str:
        text = __b64decode(text)
        self.__text_kann_mit_passwort_entschlusselt_werden(text)
        self.__text_nicht_verschluesselt_pruefung(text)
        text = text[len(self.__signaturtext)+32:]
        out_bytes = bytes()
        size = int(text[:16])
        text = text[16:]
        IV = text[:16]
        text = text[16:]
        decryptor = __AES.new(self.__get_key_from_password(), __AES.MODE_CFB, IV)
        index = 0
        while True:
            chunk = text[index: index + self.__chunks]
            if len(chunk) == 0:
                break
            out_bytes += decryptor.decrypt(chunk)
            index += self.__chunks
        return str(out_bytes[:size], encoding="utf8")

    def __str__(self) -> str:
        """Gibt den Ausgabestring des Objekts zurück"""
        return f"<AESTextEncryptor passwort={self.__passwort} signatur={self.__signaturtext} chunks={self.__chunks}>"

    def __repr__(self) -> str:
        """Gibt den Representationsstring zurück"""
        return f"AESTextEncryptor({self.__passwort}, {self.__signaturtext}, {self.__chunks})"

    def __eq__(self, other) -> bool:
        """Gibt zurück, ob das Passwort mit dem des Arguments übereinstimmt"""
        if type(other) == str:
            return self.__passwort == other
        elif type(other) == type(self):
            return self.__passwort == other.__passwort
        pass

    def __ne__(self, other) -> bool:
        """Gibt zurück, ob das Passwort von dem des Arguments verschieden ist"""
        return self.__eq__(other) is False

    def __len__(self) -> int:
        """Gibt die Länge des Passworts zurück"""
        return len(self.__passwort)

    def __get_key_from_password(self) -> bytes:
        return __SHA256.new(bytes(self.__passwort, encoding="utf8")).digest()

    def __is_encrypted(self, text):
        return bytes(self.__signaturtext, encoding="utf8") == text[:len(self.__signaturtext)]

    def __get_text_key(self, text):
        return text[len(self.__signaturtext):len(self.__signaturtext)+32]

    def __text_bereits_verschluesselt_pruefung(self, text):
        if self.__is_encrypted(text):
            raise TextIsEncrypted
        pass

    def __text_nicht_verschluesselt_pruefung(self, text):
        if self.__is_encrypted(text):
            pass
        else:
            raise TextIsNotEncrypted
        pass

    def __text_kann_mit_passwort_entschlusselt_werden(self, text):
        if self.__get_text_key(text) != __SHA256.new(self.__get_key_from_password()).digest():
            raise WrongPassword
        pass
    pass
