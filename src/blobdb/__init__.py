from blobdb import model
from blobdb import secure
from blobdb import handler

from base64 import b64encode, b64decode
from json import dumps, loads

def get_account_by_username(username: str) -> tuple[handler.account.AccountHandler | None, str]:
    """
        Finds the account model by username.
        When model is found a class is created and the model is given.
        
        TODO move status messages to central point for updates.
    """
    account_model = model.get_account_model_by_username(username)
    if account_model is not None:
        return handler.account.AccountHandler(account_model), "Success!"
    return None, "No account found!"


def create_account(username: str, password: str, email: str = "") -> tuple[handler.account.AccountHandler | None, str]:
    """
        Creates an account with the provided username, password and email.
        Checks for an existing account before attempting to create.
        
        TODO handle username, password and email validation.
        
        TODO move status messages to central point for updates.
    """
    existing_account = get_account_by_username(username)[0]
    
    if existing_account is not None:
        return None, "An account with this username already exist!"
    
    account_password, salt = secure.hash.derive_account_password(password)
    account_data_password = secure.hash.derive_account_data_password(password, salt)[0]
    
    base64_account_password = b64encode(account_password).decode()
    base64_account_salt = b64encode(salt).decode()
    
    account_model = model.create_account_model(
        username=username, 
        password=base64_account_password,
        email=email,
        salt=base64_account_salt,
    )
    
    account_data, nonce = secure.cipher.encrypt_data(
        data=dumps(
            {
                "blobs": [],
                "nonce": "",
                "key": b64encode(
                    secure.hash.get_random_bytes(32)
                ).decode()
            }
        ).encode(),
        cipher_password=account_data_password
    )
    
    base64_account_data = b64encode(account_data).decode()
    base64_account_nonce = b64encode(nonce).decode()
    
    account_model.data = base64_account_data
    account_model.nonce = base64_account_nonce
    
    account_model.save()
    
    return handler.account.AccountHandler(account_model), "Success!"