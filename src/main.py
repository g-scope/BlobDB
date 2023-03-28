# From using the hashed password, it is 64 byte value split half for data key.
import interface

from base64 import b64decode

account_handler = interface.create_account_handler(
    interface.get_account_by_username("testusername")[0],
    "testpasswwsord"
)


