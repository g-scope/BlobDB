from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from scrypt import scrypt

import json

def hash_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
        When salt is None it will generate a new salt that is 128 bytes long and return it.
        If a salt value is given it will return the same salt value.
        
        scrypt:
            N=32768
            r=8
            p=4
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


def compare_account_password(password: str, salt: bytes, hashed_password: bytes) -> bool:
    return derive_account_password(password, salt)[0] == hashed_password


def __generic_encrypt_data(password: bytes, data: dict) -> tuple[bytes, bytes]:
    cipher = AES.new(password, mode=AES.MODE_EAX)
    return cipher.encrypt(json.dumps(data).encode()), cipher.nonce


def encrypt_data(data: dict, salt: bytes = None, password: str = None, aes_password: bytes = None) -> tuple[bytes, bytes]:
    """
        for a string password it also requires a salt.
        
        If aes_password is given, it will ignore salt and password.
        aes_password has no safety checks and must be 32 chars or less.
        
        returns encrypted data, cipher nonce.
    """
    if aes_password is not None:
        return __generic_encrypt_data(aes_password, data)
    return __generic_encrypt_data(derive_account_data_password(password, salt)[0], data)


def decrypt_data(data: bytes, nonce: bytes, password: bytes) -> dict:
    """
        AES password, no other extra handling in this function.
    """
    cipher = AES.new(password, AES.MODE_EAX, nonce=nonce)
    return json.loads(cipher.decrypt(data).decode())