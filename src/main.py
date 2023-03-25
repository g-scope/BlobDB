import DBInterface

account, message = DBInterface.Manager.Account.CreateAccount(
    username="testaccount",
    password="test"
)

print(account, message)