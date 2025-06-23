import datetime
import os
from os import mkdir
from time import sleep

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from DBService import DBService
from EncryptionDecryption import EncryptorDecryptor
from InputValidation import InputValidator
from Logger import Logger, LogLevel
from Types import (Cities, Employee, HondaModels, Scooter, ScooterBrands,
                   SegwayNinebotModels, Traveller, VespaModels, XiaomiModels,
                   YamahaModels)


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

    def AddOrEditScooter(self, newScooter: Scooter, oldScooter: Scooter = None) -> bool:
        if (self.LoggedInEmployee.Role != "ServiceEngineer"):
            longest_brand = len(max(ScooterBrands, key=lambda city: len(city.value)).value)
            print(self.RepeatString("#", longest_brand + 9, ""))
            index = 1
            for brand in ScooterBrands:
                print(self.RepeatString(" ", longest_brand + 8, f"# [{index}] {brand.value}") + "#")
                index += 1
            print(self.RepeatString("#", longest_brand + 9, ""))
    
            inputStr = input("Choose the brand: ")
            if (not InputValidator.IsValidChoiceInput(inputStr, index)): return False
            newScooter.Brand = list(ScooterBrands)[int(inputStr) - 1]
            print(VespaModels)
    
            ModelList = []
            match newScooter.Brand:
                case ScooterBrands.Vespa:
                    ModelList = VespaModels
                case ScooterBrands.Yamaha:
                    ModelList = YamahaModels
                case ScooterBrands.Honda:
                    ModelList = HondaModels
                case ScooterBrands.SegwayNinebot:
                    ModelList = SegwayNinebotModels
                case _:
                    ModelList = XiaomiModels

            longest_model = len(max(ModelList, key=lambda city: len(city.value)).value)
            print(self.RepeatString("#", longest_model + 9, ""))
            index = 1
            for model in ModelList:
                print(self.RepeatString(" ", longest_model + 8, f"# [{index}] {model.value}") + "#")
                index += 1
            print(self.RepeatString("#", longest_model + 9, ""))

            inputStr = input("Choose the model: ")
            if (not InputValidator.IsValidChoiceInput(inputStr, index)): return False
            newScooter.Model = (list(ModelList)[int(inputStr) - 1])
            #newTraveler.City = list(Cities)[int(inputStr) - 1]

            inputStr = input("Input the serie number (ahnumeric chars 10-17): ")
            if (not InputValidator.IsValidSerialNumber(inputStr)): return False
            newScooter.SerialNumber = inputStr
            inputStr = input("Topspeed of scooter: ")
            if (not InputValidator.IsValidNumber(inputStr)): return False
            newScooter.TopSpeed = (float(inputStr))
            inputStr = input("Battery capacity of scooter: ")
            if (not InputValidator.IsValidNumber(inputStr)): return False
            newScooter.BatteryCapacity = (inputStr)
        else:
            newScooter.Brand = oldScooter.Brand
            newScooter.Model = oldScooter.Model
            newScooter.SerialNumber = oldScooter.SerialNumber
            newScooter.TopSpeed = oldScooter.TopSpeed
            newScooter.BatteryCapacity = oldScooter.BatteryCapacity
        
        inputStr = input("State of Charge (SoC) of scooter: ")
        if (not InputValidator.IsValidPercentage(inputStr)): return False
        newScooter.StateOfCharge = (inputStr)
        inputStr = input("Max Target-range SoC of scooter: ")
        if (not InputValidator.IsValidPercentage(inputStr)): return False
        newScooter.TargetRangeMax = (inputStr)
        inputStr = input("Min Target-range SoC of scooter: ")
        if (not InputValidator.IsValidPercentage(inputStr)): return False
        newScooter.TargetRangeMin = (inputStr)
        inputStr = input("Latitude of scooter: ")
        if (not InputValidator.IsValidLatitude(inputStr)): return False
        newScooter.LocationLat = (float(inputStr))
        inputStr = input("Longitude of scooter: ")
        if (not InputValidator.IsValidLongitude(inputStr)): return False
        newScooter.LocationLat = (float(inputStr))
        inputStr = input("Is scooter out of service (Y, yes, N no): ")
        if (not InputValidator.IsValidYesNo(inputStr)): return False
        if (inputStr.lower() == "yes" or inputStr.lower() == "y"): newScooter.OutOfService = True
        else: newScooter.OutOfService = (False)
        inputStr = input("Milage of scooter: ")
        if (not InputValidator.IsValidNumber(inputStr)): return False
        newScooter.Mileage = (float(inputStr))
        inputStr = input("Last maintenance date (YYYY-MM-DD): ")
        if (not InputValidator.IsValidDate(inputStr)): return False
        newScooter.LastMaintenanceDate = inputStr
        return True


    def AddOrEditTraveller(self, newTraveler: Traveller) -> bool:
            inputStr = input("Firstname of traveler: ")
            if (not InputValidator.IsValidName(inputStr)): return False
            newTraveler.Firstname = inputStr
            inputStr = input("Lastname of traveler: ")
            if (not InputValidator.IsValidName(inputStr)): return False
            newTraveler.Lastname = inputStr
            inputStr = input("Birthday of traveler (YYYY-MM-DD): ")
            if (not InputValidator.IsValidDate(inputStr)): return False
            newTraveler.Birthday = inputStr
            inputStr = input("Gender of traveler M/F: ")
            if (not InputValidator.IsValidGender(inputStr)): return False
            newTraveler.Gender = inputStr
            inputStr = input("Streetname: ")        #needs input checking!!!
            newTraveler.StreetName = inputStr
            inputStr = input("HouseNumber: ")
            if (not InputValidator.IsValidHouseNumber(inputStr)): return False
            newTraveler.HouseNumber = inputStr
            inputStr = input("ZipCode: ")
            if (not InputValidator.IsValidZipCode(inputStr)): return False
            newTraveler.ZipCode = inputStr


            longest_city = len(max(Cities, key=lambda city: len(city.value)).value)
            print(self.RepeatString("#", longest_city + 9, ""))
            index = 1
            for brand in Cities:
                print(self.RepeatString(" ", longest_city + 8, f"# [{index}] {brand.value}") + "#")
                index += 1
            print(self.RepeatString("#", longest_city + 9, ""))
    
            inputStr = input("Choose the city: ")
            if (not InputValidator.IsValidChoiceInput(inputStr, index)): return False
            newTraveler.City = list(Cities)[int(inputStr) - 1]


            inputStr = input("Email: ")
            if (not InputValidator.IsValidEmail(inputStr)): return False
            newTraveler.Email = inputStr
            inputStr = input("PhoneNumber (+31-6-12345678): ")
            if (not InputValidator.IsValidPhoneNumber(inputStr)): return False
            newTraveler.PhoneNumber = inputStr
            inputStr = input("DrivingLicenseNumber (XXddddddd or Xdddddddd): ")
            if (not InputValidator.IsValidDrivingLicenseNumber(inputStr)): return False
            newTraveler.DrivingLicenseNumber = inputStr
            inputStr = input("RegistrationDate: ")
            if (not InputValidator.IsValidDate(inputStr)): return False
            newTraveler.RegistrationDate = inputStr
            return True