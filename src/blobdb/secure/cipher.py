from Crypto.Cipher import AES
from blobdb.secure import hash

def __generic_decrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    return AES.new(key, AES.MODE_EAX, nonce=nonce).decrypt(data)


def __generic_encrypt(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.encrypt(data), cipher.nonce


def encrypt_data(
    data: bytes,
    password: str | None = None, 
    salt: bytes | None = None, 
    cipher_password: bytes | None = None
) -> tuple[bytes, bytes, bytes | None]:
    """
        password is ran through derive_account_data_password for the encryption key.
        If salt is missing, it will generate a new one and use it for the encryption key.
        
        If cipher_password is given, it will ignore password and salt.
        If a password is given, it will use or generate a salt.
        
        no salt will be returned if cipher_password is given.
        
        returns a tuple(
            bytes: encrypted_data,
            bytes: nonce,
            bytes: salt(None if cipher_password provided)
        )
    """
    if cipher_password is not None:
        return __generic_encrypt(data, cipher_password)
    
    cipher_password, salt = hash.derive_account_data_password(
        password,
        salt
    )
    
    encrypted_data, nonce = __generic_encrypt(data, cipher_password)
    
    return encrypted_data, nonce, salt


def decrypt_data(
    data: bytes,
    nonce: bytes,
    password: str | None = None,
    salt: bytes | None = None,
    cipher_password: bytes | None = None
) -> bytes:
    """
        password is ran through derive_account_data_password for the decryption key.
        If cipher_password is given, it will ignore password and salt.
        
        If a password is given, a salt is required or it will error!
        
        returns bytes: decrypted_data
        (even with the wrong password/salt it will return data)
    """
    if cipher_password is not None:
        return __generic_decrypt(data, cipher_password, nonce)
        
    if password is not None and salt is None:
        raise Exception("Password provided but no salt!")
    
    cipher_password, salt = hash.derive_account_data_password(
        password,
        salt
    )
    
    return __generic_decrypt(data, cipher_password, nonce)
    
    