import DBInterface

account, message = DBInterface.Manager.Account.CreateAccount(
    username="testaccount",
    password="tesadfasdfst"
)

print(account, message)