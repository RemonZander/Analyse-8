from os import mkdir
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
class EncryptorDecryptor(object):
    try:
        mkdir("./keys")
    except:
        pass
    
    private_key = ""
    public_key = ""      
    
    if (not os.path.isfile("./keys/private_key.pem")):       
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open("./keys/private_key.pem", 'wb') as f:
            f.write(pem) 

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open("./keys/public_key.pem", 'wb') as f:
            f.write(pem)
    else:
        with open("./keys/private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            ) 
            
        with open("./keys/public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )   
    
    def Encrypt(self, data):      
        return self.public_key.encrypt(
            str(data).encode('utf-8'),            
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def Decrypt(self, data):
        return self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode("utf-8")