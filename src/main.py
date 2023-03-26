# From using the hashed password, it is 64 byte value split half for data key.
import interface

account, message = interface.create_account(
    username="testusername",
    password="testpassword"
)

print(account)
print(message)