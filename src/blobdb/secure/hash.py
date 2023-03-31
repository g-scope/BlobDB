from Crypto.Random import get_random_bytes
from scrypt import scrypt

# TODO replace static numbers with a function getting their number.
DEFAULT_SCRYPT_SALT_LENGTH = 128
DEFAULT_SCRYPT_N = 131072
DEFAULT_SCRYPT_R = 4
DEFAULT_SCRYPT_P = 1

def hash_password(password: str | bytes, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """
        Hashes the password using scrypt.
        If a salt is not provided a new one will be generated and used.
        
        salt length: 128 bytes
        
        scrypt N: 131072
        scrypt R: 8
        scrypt P: 4
        
        returns a tuple(
            bytes: hashed_password,
            bytes: password_salt
        )
    """
    if type(password) is str:
        password = password.encode()
    if salt is None:
        salt = get_random_bytes(DEFAULT_SCRYPT_SALT_LENGTH)
    return scrypt.hash(password, salt, N=DEFAULT_SCRYPT_N, r=DEFAULT_SCRYPT_R, p=DEFAULT_SCRYPT_P), salt


def derive_account_password(password: str | bytes, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """        
        [MUST READ]
            !NEVER USE THIS ACCOUNT PASSWORD FOR ENCRYPTION!
            
            
            This account password is used STRICTLY for authentication/comparison.
            
            
            For an encryption key/password use derive_account_data_password.
        
        Hashes the password using hash_password(scrypt).
        If a salt is not provided a new one will be generated and used.
        
        The account password is the FIRST 32 bytes of the hashed password.
        
        returns a tuple(
            bytes: account_password,
            bytes: password_salt
        )
    """
    hashed_password, salt = hash_password(password, salt)
    return hashed_password[32:], salt


def derive_account_data_password(password: str | bytes, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """
    [MUST READ]
        !NEVER SAVE THIS PASSWORD ANYWHERE!
        
        This password should only exist in memory and never in disk!
    
    Hashes the password using hash_password(scrypt).
    If a salt is not provided a new one will be generated and used.
        
    The account password is the LAST 32 bytes of the hashed password.
        
    returns a tuple(
        bytes: account_data_password,
        bytes: password_salt
    )
    """
    hashed_password, salt = hash_password(password, salt)
    return hashed_password[:32], salt


