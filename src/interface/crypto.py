from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from scrypt import scrypt

import json, base64

def hash_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
        When salt is None it will generate a new salt that is 128 bytes long and return it.
        If a salt value is given it will return the same salt value.
    """
    if salt is None:
        salt = get_random_bytes(128)
    return scrypt.hash(password, salt, N=32768, r=8, p=4), salt


def derive_account_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
        Returns 32 bytes when successful. Uses hash_password then extracts the first half of the hashed_password..
    """
    hashed_password, salt = hash_password(password, salt)
    account_password = hashed_password[32:]
    return account_password, salt


def derive_account_data_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
        Returns 32 bytes when successful. Uses hash_password then extracts the last half of the hashed_password..
    """
    hashed_password, salt = hash_password(password, salt)
    account_password = hashed_password[:32]
    return account_password, salt


def compare_password(password: str, salt: bytes, hashed_password: bytes) -> bool:
    return hash_password(password, salt)[0] == hashed_password


def encrypt_data(password: str, salt: bytes, data: dict) -> tuple[bytes, bytes]:
    cipher = AES.new(derive_account_data_password(password, salt)[0], mode=AES.MODE_EAX)
    return cipher.encrypt(json.dumps(data).encode()), cipher.nonce