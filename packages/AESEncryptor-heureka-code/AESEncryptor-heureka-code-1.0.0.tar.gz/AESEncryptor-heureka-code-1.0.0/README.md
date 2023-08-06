#Diese Packet enthält Klassen zum Ver- und Entschlüsseln von Datein und Texten.

##class AESFileEncryptor:
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
##class AESTextEncryptor:
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
##Exceptions, die ausgelöst werden können
###Datei Exceptions:

    FileError:
        ist die Klasse, von der die anderen File-Exceptions erben.

    FileIsEncrypted:
        wird ausgelöst, wenn eine Datei reschlüsselt werden soll, die bereits verschlüsselt worden ist.

    FileIsNotEncrypted:
        wird ausgelöst, wenn eine Datei entschlüsselt werden soll, die nicht entschlüsselbar ist.
###Passwort Exceptions:

    PasswordError:
        ist die Klasse, von der die anderen Passwort-Exceptions erben.

    WrongPassword:
        ist die Exception, falls ein falsches Passwort verwendet wurde.
###Text Exceptions:

    TextError:
        ist die Klasse, von der die anderen Text Exceptions erben.

    TextIsEncrypted:
        wird ausgelöst, wenn der Text nicht verschlüsselt werden kann, weil er das bereits wurde.

    TextIsNotEncrypted:
        wird ausgelöst, wenn Text entschlüsselt werden soll, der gar nicht verschlüsselt worden ist.