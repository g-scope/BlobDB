from uuid import uuid4
from math import floor
from json import loads, dumps

from base64 import b64decode, b64encode
from blobdb import model, secure

class AccountHandler:
    def __init__(self, account: model.AccountModel, password: str | bytes | None = None):
        self.account_model: model.AccountModel = account
        self.account_password: bytes | str | None = password
        self.account_authorized: bool = False
    
    
    def authorize(self, password: str | bytes, remember_password: bool = False, override: bool = False) -> bool:
        salt = b64decode(self.account_model.salt)
        if b64decode(self.account_model.password) == secure.hash.derive_account_password(password, salt)[0] or override:
            self.account_authorized = True
            if remember_password:
                self.account_password = password
            return True
        return False
    
    
    def load_pointer_data(self) -> dict:
        return loads(
            secure.cipher.decrypt_data(
                data=b64decode(self.account_model.data),
                nonce=b64decode(self.account_model.nonce),
                salt=b64decode(self.account_model.salt),
                password=self.account_password,
            )
        )
    
    
    def save_pointer_data(self, data: bytes) -> bool:
        if self.account_authorized and self.account_password is not None:
            if self.authorize(self.account_password):
                new_encrypted_pointer_data, nonce, salt = secure.cipher.encrypt_data(
                    data,
                    self.account_password
                )
                
                account_password = secure.hash.derive_account_password(self.account_password, salt)[0]
                
                self.account_model.password = b64encode(account_password).decode()
                self.account_model.salt = b64encode(salt).decode()
                
                self.account_model.nonce = b64encode(nonce).decode()
                self.account_model.data = b64encode(new_encrypted_pointer_data).decode()
                
                self.account_model.save()
                
                return True
            return False
        return False
    
    def load_vault_data(self) -> bytes:
        if self.account_authorized and self.account_password is not None:
            pointer_data = self.load_pointer_data()
            
            aes_key = b64decode(pointer_data.get("key"))
            blob_id_list = pointer_data.get("blobs")
            
            built_data_string = ""
            next_position = 0
            length = len(blob_id_list)
            
            while length != 0:
                for blob_id, position in blob_id_list:
                    if position == next_position:
                        # TODO setup a function to get a blobmodel and create error handling for missing blobs
                        built_data_string = built_data_string + model.BlobModel.get(model.BlobModel.bid==blob_id).data
                        next_position += 1
                        length -= 1
            
            decrypted_data = secure.cipher.decrypt_data(
                b64decode(built_data_string),
                b64decode(pointer_data.get("nonce")),
                cipher_password=aes_key
            )
            
            return decrypted_data
            
        return b""
    
    def save_vault_data(self, data: bytes, password: str | bytes | None = None) -> bool:
        password = password or self.account_password
        if password is not None and self.authorize(password, remember_password=True):
            
            new_vault_password = secure.hash.get_random_bytes(32)
            
            # Loading & Overwritting base info
            pointer_data = self.load_pointer_data()
            
            encrypted_data, nonce = secure.cipher.encrypt_data(
                data,
                cipher_password=new_vault_password
            )
            
            pointer_data["key"] = b64encode(new_vault_password).decode()
            pointer_data["nonce"] = b64encode(nonce).decode()
            # Finish overwriting base info loading blobs
            
            base64_encrypted_data = b64encode(encrypted_data).decode()
            
            divide_index = floor(len(base64_encrypted_data) / 2)
            
            blob_data_a = base64_encrypted_data[:divide_index]
            blob_data_b = base64_encrypted_data[divide_index:]
            
            blob_a = model.BlobModel.create(
                bid=uuid4().hex,
                data=blob_data_a
            )
            
            blob_b = model.BlobModel.create(
                bid=uuid4().hex,
                data=blob_data_b
            )
            
            blob_a.save()
            blob_b.save()
            
            pointer_data["blobs"] = [[blob_a.bid, 0], [blob_b.bid, 1]]
            
            self.save_pointer_data(dumps(pointer_data).encode())
            
            return True
            

           
    