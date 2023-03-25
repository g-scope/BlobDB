def UsernameTooShort(username: str = None) -> str:
    if username != None:
        return f"'{username}' is too short!"
    return "Your username is too short!"


def UsernameTooLong() -> str:
    return "Your username is too long!"


def UsernameBypass() -> str:
    return "Username bypassed!"


def UsernameSuccess() -> str:
    return "Username valid!"


def PasswordTooShort() -> str:
    return "Your password is too short!"


def PasswordTooLong() -> str:
    return "Your password is too long!"


def PasswordBypass() -> str:
    return "Password bypassed!"


def PasswordSuccess() -> str:
    return "Password valid!"


def CreateAccountSuccess() -> str:
    return "Account successfully created!"


def CreateAccountFailAlreadyExists() -> str:
    return "An account with that username already exists!"


def GetAccountRanWithoutError() -> str:
    return "Request ran without errors."


def GetAccountRanWithError() -> str:
    return "Request ran with errors."