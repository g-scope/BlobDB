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


def CreateAccountSuccess() -> str:
    return "Account successfully created!"


def CreateAccountFailAlreadyExists() -> str:
    return "An account with that username already exists!"


def GetAccountRanWithoutError() -> str:
    return "Request ran without errors."