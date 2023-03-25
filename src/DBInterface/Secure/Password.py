from Crypto.Random import get_random_bytes
from scrypt import scrypt

# TODO, config reference for default salt length
def HashPassword(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = get_random_bytes(32)
    
    return scrypt.hash(
        password=password,
        salt=salt
    ), salt
    
    
def PasswordMatches(password: str, salt: bytes, hashed_password: bytes) -> bool:
    compare_password, _ = HashPassword(password=password, salt=salt)
    return compare_password == hashed_password