import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="AESEncryptor-heureka-code",
    version="1.0.0",
    install_requires=["pycryptodome"],
    author="heureka-code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    description="Verschlüsselt Datein und Texte mit AES",
    url="https://github.com/heureka-code/AESEncryptor-heureka-code",
    download_url="https://github.com/heureka-code/AESEncryptor-heureka-code/archive/refs/tags/1.0.0.tar.gz",
    packages=setuptools.find_packages()
    )
