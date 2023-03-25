from base64 import b64encode, b64decode
from .. import Validator, Messages, Secure, Models

def GetAccountByUsername(username: str) -> tuple[Models.Account | None, str]:
    valid, message = Validator.Account.UsernameValid(username=username)
    
    if not valid:
        return None, message
    
    account = None
    message = Messages.Account.GetAccountRanWithoutError()
    
    try:
        account = Models.Account.get(Models.Account.username==username)
    except:
        message = Messages.Account.GetAccountRanWithError()
    
    return account, message


def CreateAccount(username: str, password: str, email: str = "") -> tuple[Models.Account | None, str]:
    username_valid, username_message = Validator.Account.UsernameValid(username=username)
    password_valid, password_message = Validator.Account.PasswordValid(password=password)
    
    if not username_valid:
        return None, username_message
    
    if not password_valid:
        return None, password_message
    
    account, _ = GetAccountByUsername(
        username=username
    )
    
    if account:
        return None, Messages.Account.CreateAccountFailAlreadyExists()
    
    hashed_password, password_salt = Secure.Password.HashPassword(
        password=password
    )
    
    hashed_password_b64 = b64encode(hashed_password).decode()
    password_salt_b64 = b64encode(password_salt).decode()
    
    account = Models.Account.create(
        username=username,
        password=hashed_password_b64,
        salt=password_salt_b64
    )
    
    account.save()
    
    return account, Messages.Account.CreateAccountSuccess()