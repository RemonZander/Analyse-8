import re
from datetime import datetime

class InputValidator:
    @staticmethod
    def IsValidZipCode(zip_code: str) -> bool:
        """
        Validates Dutch zip code: 4 digits followed by 2 uppercase letters.
        Example: 1234AB
        """
        regex = r"\d{4}[A-Z]{2}"
        if re.fullmatch(regex, zip_code):
            return True
        return False

    @staticmethod
    def IsValidPhoneNumber(phone: str) -> bool:
        """
        Validates Dutch mobile phone number.
        Format: +31-6-12345678
        """

        regex = r"\+31-6-\d{8}"
        if re.fullmatch(regex, phone):
            return True
        return False

    @staticmethod
    def IsValidDrivingLicenseNumber(license_num: str) -> bool:
        """
        Validates driving license number.
        Format: XXddddddd or Xdddddddd
        Example: AB1234567 or A12345678
        """

        regex = r"[A-Z]{2}\d{7}|[A-Z]{1}\d{8}"
        if (re.fullmatch(regex, license_num)):
            return True
        return False

    @staticmethod
    def IsValidSerialNumber(serial: str) -> bool:
        """
        Validates scooter serial number.
        10 to 17 alphanumeric characters.
        """
        
        regex = r"[A-Za-z0-9]{10,17}"
        if re.fullmatch(regex, serial):
            return True
        return False

    @staticmethod
    def IsValidDate(date_string: str) -> bool:
        """
        Validates date format YYYY-MM-DD and checks if it's a real date.
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def IsValidUsername(username: str) -> bool:
        """
        Validates custom identifier:
        - Length between 8 and 10 characters
        - Must contain at least one letter or underscore
        - Allowed characters: letters, numbers, underscore (_), apostrophe ('), dot (.)
        """
        regex = r"[a-zA-Z0-9_.']{8,10}"
        if re.fullmatch(regex, username) or username == "super_admin":
            return True
        return False

    @staticmethod
    def IsValidPassword(password: str) -> bool:
        """
        Validates password:
        - At least 8 characters
        - At least one uppercase, one lowercase, one digit, one special char
        - Must not contain spaces
        """
        regex = r"^(?=.{8,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S+$"
        if re.fullmatch(regex, password):
            return True
        return False

    @staticmethod
    def IsValidEmail(email: str) -> bool:
        regex = r"[^@]+@[^@]+\.[^@]+"
        if re.fullmatch(regex, email):
            return True
        return False

    @staticmethod
    def IsValidGender(gender: str) -> bool:
        return gender.upper() in ["M", "F"]

    @staticmethod
    def IsValidHouseNumber(house_number: str) -> bool:
        regex = r"\d+[a-zA-Z]?"
        if re.fullmatch(regex, house_number):
            return True
        return False

    @staticmethod
    def IsValidChoiceInput(choice : int, maxChoice: int) -> bool:
        """
        Validates menu input: must be an integer between 1 and max.
        """
        try:
            choice = int(choice)
        except :
            return False
        if(choice >= 0 and choice <= maxChoice):
            return True
        return False

    @staticmethod
    def IsValidName(name: str) -> bool:
        """
        Validates name:
        - 1 to 20 characters
        - Only letters
        """
        regex = r"[A-Za-z]{1,20}"
        if re.fullmatch(regex, name):
            return True
        return False

    @staticmethod
    def IsValidNumber(number: str) -> bool:
        """
            Validates that the input is a number
            This can be an int or float
        """
        regex = r"^(?:0|[1-9]\d*)(?:,\d+)?$"
        if re.fullmatch(regex, number):
            return True
        return False

    @staticmethod
    def IsValidPercentage(percent: str) -> bool:
        """
            Validates that the input is a valid percentage
            - should be this format 30%
            - should be this format 3,7%
        """
        regex = r"^(?:100|(?:0|[1-9]\d?))(?:,\d+)?%$"
        if re.fullmatch(regex, percent):
            return True
        return False

    @staticmethod
    def IsValidLatitude(latitude: str) -> bool:
        """
            Checks if the input is a valid latitude
            - should have 5 decimals aftewr the comma
            - should be between -90 and 90
        """
        regex = r"^-?(?:[0-8]?\d(?:,\d{5})?|90(?:,0{5})?)$"
        if re.fullmatch(regex, latitude):
            return True
        return False

    @staticmethod
    def IsValidLongitude(Longitude: str) -> bool:
        """
            Checks if the input is a valid Longitude
            - should have 5 decimals aftewr the comma
            - should be between -180 and 180
        """

        regex = r"^-?(?:1?[0-7]?\d(?:,\d{5})?|180(?:,0{5})?)$"
        if re.fullmatch(regex, Longitude):
            return True
        return False

    @staticmethod
    def IsValidYesNo(choice: str) -> bool:
        """
            Checks if the input is of type Y or y or Yes or yes or N or n or No or no
        """
        regex = r"^(?i)(y|yes|n|no)$"
        if re.fullmatch(regex, choice):
            return True
        return False
    
    @staticmethod
    def IsValidSearchInput(search_string: str) -> bool:
        regex = r"[A-Za-z0-9\s.,@\-+!?:;'\"()/_]*"
        if 1 <= len(search_string) <= 100 and re.fullmatch(regex, search_string):
            return True
        return False
    
    @staticmethod
    def IsValidBackupCode(BackUpCode: str) -> bool:
        """
            Check if input is valid:
            - should be between 4 and 40 characters
            - could contain letters, numbers, and special characters
            - should not contain spaces
        """
        regex = r"[A-Za-z0-9!@#$%^&*(),.?\":{}|<>_\-+=]*"
        if re.fullmatch(regex, BackUpCode) and 4 <= len(BackUpCode) <= 40:
            return True
        return False