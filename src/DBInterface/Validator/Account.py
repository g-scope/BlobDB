from .. import Messages

def UsernameValid(username: str, bypass: bool = False) -> tuple[bool, str]:
    # TODO add json/config reference for lengths & other checks.
    if bypass:
        return True, Messages.Account.UsernameBypass()
    
    if len(username) < 8:
        return False, Messages.Account.UsernameTooShort(
            username=username
        )
    
    if len(username) > 64:
        return False, Messages.Account.UsernameTooLong()

    # TODO illegal character check.
    
    return True, Messages.Account.UsernameSuccess()


def PasswordValid(password: str, bypass: bool = False) -> tuple[bool, str]:
    if bypass:
        return True, Messages.Account.PasswordBypass()
    
    if len(password) < 8:
        return False, Messages.Account.PasswordTooShort()
    
    if len(password) > 64:
        return False, Messages.Account.PasswordTooLong()
    
    # TODO minimum security requirements for chars.
    # upper, symbols.
    
    return True, Messages.Account.PasswordSuccess()