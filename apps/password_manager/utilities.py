from cryptography.fernet import Fernet
from bv_timer.settings import ENCRYPTED_KEY


def encryptString(password):

    crypter = Fernet(ENCRYPTED_KEY.encode())
    pw = crypter.encrypt(str.encode(password))

    return pw.decode()


def decryptString(password):

    crypter = Fernet(ENCRYPTED_KEY.encode())
    pw = crypter.decrypt(password)

    return pw.decode()