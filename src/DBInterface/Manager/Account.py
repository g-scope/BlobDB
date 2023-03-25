from base64 import b64encode, b64decode
from .. import Validator, Messages, Secure, Models

def GetAccountByUsername(username: str) -> tuple[Models.Account | None, str]:
    valid, message = Validator.Account.UsernameValid(username=username)
    
    if not valid:
        return None, message
    
    account = None
    
    try:
        account = Models.Account.get(Models.Account.username==username)
    except:
        pass
    
    return account, Messages.Account.GetAccountRanWithoutError()


def CreateAccount(username: str, password: str, email: str = "") -> tuple[Models.Account | None, str]:
    valid, message = Validator.Account.UsernameValid(username=username)
    
    if not valid:
        return None, message
    
    account, message = GetAccountByUsername(
        username=username
    )
    
    if account:
        return None, Messages.Account.CreateAccountFailAlreadyExists()
    
    account = Models.Account.create(username=username)
    
    # TODO Secure Module.
    
    
    account.save()
    
    return account, Messages.Account.CreateAccountSuccess()