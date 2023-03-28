from base64 import b64decode

from interface import models
from interface import crypto
from interface import messages

class AccountHandler:
    def __init__(self, account: models.AccountModel, password: str):
        self.success = False
        
        try:
            self.key = crypto.derive_account_data_password(
                password,
                b64decode(account.salt)
            )
            
            self.data = crypto.decrypt_data(
                b64decode(account.data),
                b64decode(account.nonce),
                self.key
            )
        except:
            pass
        finally:
            self.success = True
            print("decrypted and verified?")
            
            self.account: models.AccountModel = account
            
            # XOR shift key for memory safety?
            self.key: bytes = None
        
    
        