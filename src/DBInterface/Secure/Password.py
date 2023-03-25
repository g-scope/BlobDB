from Crypto.Random import get_random_bytes
from scrypt import scrypt

# TODO, config reference for default salt length
def HashPassword(password: str, salt: bytes = get_random_bytes(32)) -> tuple[bytes, bytes]:
    return scrypt.hash(
        password=password,
        salt=salt
    ), salt
    
    
    