from randomuser import RandomUser
from json import dumps

import string, random

import blobdb

"""
def generator() -> str:
    return "!" + ''.join(random.choices(string.ascii_letters, k=4)) + "!" + ''.join(random.choices(string.ascii_letters, k=4)) + "!"    

for _ in range(0, 100):
    username = generator()
    password = generator()
    email = generator()
    
    account, message = blobdb.create_account(username, password, email)
    print(account, message, username)
    
    account.save_vault_data(
        dumps({
            "secret data": generator(),
            "oopsy": generator(),
            "huh": generator()
        }).encode(),
        password
    )
    
    with open("log.txt", "a") as file:
        file.write(f"{username}:{password}\n")
        file.close()

"""
accounts = []

with open("log.txt", "r") as file:
    for account in file.read().split("\n"):
        if len(account) > 3:
            accounts.append(account.split(":"))
    file.close()


for username, password in accounts:
    handler = blobdb.get_account_by_username(username)[0]
    
    if handler.authorize(password, remember_password=True):
        print(f"[{username}] was able to be logged in! Lets tryin getting our data!")
        vault_data = handler.load_vault_data()
        print(f"[{username}] we retrieved: {vault_data}")
#"""