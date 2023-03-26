# From using the hashed password, it is 64 byte value split half for data key.
from base64 import b64encode

import interface

plaintext_master_password = "masterpassword"



account_password, account_salt = interface.derive_account_password(
    password=plaintext_master_password,
)

print(account_password, account_salt)

encrypted_data, nonce = interface.encrypt_data(
    password=plaintext_master_password,
    salt=account_salt,
    data={
        "good evening": [
            "i",
            "contain",
            "text"
        ],
        "josh": {
            "is": "gay"
        }
    }
)

print(encrypted_data)
print(nonce)