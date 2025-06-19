from os import mkdir
from Types import Employee
from DBService import DBService
#import logging
import os
import datetime
from Logger import LogLevel
from Logger import Logger
from EncryptionDecryption import EncryptorDecryptor
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
class Screen(object):
     
    try:
        mkdir("./logs")
    except :
        pass

    try:
        mkdir("./backups")
    except :
        pass    
    
    logger = Logger("./logs/", "ab")
    DB = DBService()
    encryptorDecryptor = EncryptorDecryptor()    
    DB.SetupDatabase()
    LoggedInEmployee = Employee()

    def RepeatString(self, inputString: str, maxLength: int, currentString: str):
        return f"{currentString + inputString * (maxLength - len(currentString))}"
    
    def Logger(self, employee: str, activity: str, extraInfo: str, Suspicious: str, loglevel = LogLevel.INFO):
        if (self.LoggedInEmployee.Username == "super_admin" or loglevel == LogLevel.WARNING):
            self.logger.Log(self.encryptorDecryptor.Encrypt(f"{employee} - {activity} - {extraInfo} - {Suspicious}"), LogLevel.WARNING)
        else:
            self.logger.Log(self.encryptorDecryptor.Encrypt(f"{employee} - {activity} - {extraInfo} - {Suspicious}"), loglevel)