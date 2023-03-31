import blobdb, json

# Create your account, returns a handler with some handy functions.
account_handler, message = blobdb.create_account(
    "yourusername",
    "yourpassword",
    "email@optional.com"
)

# Your data!
secret_data = {
    "your": "secret data",
    "this": "will get broken up into two blobs in the database.",
    "it": "will not have any reference to this account unless you decrypt the pointer data.",
    "the": "nonce is also stored in the pointer data."
}

# remember_password stores the password in the class. 
# I plan to make this more memory safe in the future(XOR shifting).
account_handler.authorize("yourpassword", remember_password=True)

# Password arg not required when remember_password used.
account_handler.save_vault_data(
    json.dumps(secret_data).encode()
)

# Check to see if the data you set has been retrieved properly.
data_result = account_handler.load_vault_data()

print(data_result)