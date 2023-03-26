from interface import models
from interface import crypto
from interface import messages

from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def get_account_by_username(username: str) -> tuple[models.AccountModel | None, str]:
    # TODO username string sanitization?
    account = None
    
    try:
        account = models.AccountModel.get(
            models.AccountModel.username==username
        )
    except:
        pass
    
    if account is None:
        return None, messages.ACC_RETRIEVAL_FAILURE
    
    return account, messages.ACC_RETRIEVAL_SUCCESS


def create_account(username: str, password: str) -> tuple[models.AccountModel | None, str]:
    # TODO handle username, password validation
    existing_account, _ = get_account_by_username(username)

    if existing_account is not None:
        return None, messages.ACC_CREATION_FAIL_EXISTING_ACCOUNT
    
    account_password, salt = crypto.derive_account_password(password)
    account_data_password, _ = crypto.derive_account_data_password(password, salt)

    data, nonce = crypto.encrypt_data(
        aes_password=account_data_password,
        data={
            "blobs": [],
            "key": b64encode(get_random_bytes(32)).decode()
        }
    )
    
    base64_account_password = b64encode(account_password).decode()
    base64_salt = b64encode(salt).decode()
    base64_data = b64encode(data).decode()
    base64_nonce = b64encode(nonce).decode()
    
    new_account = models.AccountModel.create(
        username=username,
        password=base64_account_password,
        salt=base64_salt,
        data=base64_data,
        nonce=base64_nonce
    )
    
    new_account.save()
    
    return new_account, messages.ACC_CREATION_SUCCESS