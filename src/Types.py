class Employee(object):
    def __init__(self, ID = None, Firstname: str = None, Lastname: str = None, Role: str = None, Username: str = None, Password = None, IsTempPwd: int = None):
        self.ID = ID
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Role = Role
        self.Username = Username
        self.Password = Password
        self.IsTempPwd = IsTempPwd

class Address(object):
    def __init__(self, StreetName: str = None, HouseNumber: str = None, ZipCode:str = None, City: str = None):
        self.StreetName = StreetName
        self.HouseNumber = HouseNumber
        self.ZipCode = ZipCode
        self.City = City

class Member(object):
    def __init__(self, UID: str = None, Firstname: str = None, Lastname:str = None, Age: int = None, Gender: str = None, Weight: float = None, Address: Address = None, Email: str = None, PhoneNumber: str = None):
        self.UID = UID
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Age = Age
        self.Gender = Gender
        self.Weight = Weight
        self.Address = Address
        self.Email = Email
        self.PhoneNumber = PhoneNumber                                