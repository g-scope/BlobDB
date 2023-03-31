from blobdb.model.blob import BlobModel
from blobdb.model.account import AccountModel

def get_account_model_by_username(username: str) -> AccountModel | None:
    """
        Returns a peewee class AccountModel.
        Errors are wrapped.
        
        TODO: add error logging for exceptions.
    """
    account = None
    try:
        account = AccountModel.get(
            AccountModel.username==username
        )
    except:
        pass
    return account


def create_account_model(username: str, password: str, salt: str, email: str) -> AccountModel | None:
    """
        Creates a new AccountModel with the provided credentials.
        It is expected that the password is either hashed or from derive_account_password.
        
        This also checks for an existing account before creating as a safety precaution.
    """
    
    existing_account_model = get_account_model_by_username(username)
    
    if existing_account_model is not None:
        return None
    
    return AccountModel.create(
        username=username,
        password=password,
        email=email,
        salt=salt,
    )

BlobModel.create_table()
AccountModel.create_table()