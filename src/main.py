import DBInterface

account, message = DBInterface.Manager.Account.GetAccountByUsername(
    username="testaccount",
)

print(
    DBInterface.Manager.Account.AuthenticateAccount(
        account=account,
        password="tesadfasdfst"
    )
)