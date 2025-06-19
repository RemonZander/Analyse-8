from typing import Optional
from datetime import datetime
from enum import Enum

class Traveller:
    def __init__(
        self,
        CustomerID: Optional[str] = None,
        Firstname: str = None,
        Lastname: str = None,
        Birthday: str = None,
        Gender: str = None,
        StreetName: str = None,
        HouseNumber: str = None,
        ZipCode: str = None,
        City: str = None,
        Email: str = None,
        PhoneNumber: str = None,
        DrivingLicenseNumber: str = None,
        RegistrationDate: str = None,
    ):
        self.CustomerID = CustomerID
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Birthday = Birthday
        self.Gender = Gender
        self.StreetName = StreetName
        self.HouseNumber = HouseNumber
        self.ZipCode = ZipCode
        self.City = City
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.DrivingLicenseNumber = DrivingLicenseNumber
        self.RegistrationDate = RegistrationDate or datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Scooter:
    def __init__(
        self,
        ID: Optional[int] = None,
        Brand: str = None,
        Model: str = None,
        SerialNumber: str = None,
        TopSpeed: float = None,
        BatteryCapacity: float = None,
        StateOfCharge: str = None,
        TargetRangeMin: int = None,
        TargetRangeMax: int = None,
        LocationLat: float = None,
        LocationLong: float = None,
        OutOfService: bool = False,
        Mileage: float = 0.0,
        LastMaintenanceDate: str = None,
        InServiceDate: str = None
    ):
        self.ID = ID
        self.Brand = Brand
        self.Model = Model
        self.SerialNumber = SerialNumber
        self.TopSpeed = TopSpeed
        self.BatteryCapacity = BatteryCapacity
        self.StateOfCharge = StateOfCharge
        self.TargetRangeMin = TargetRangeMin
        self.TargetRangeMax = TargetRangeMax
        self.LocationLat = LocationLat
        self.LocationLong = LocationLong
        self.OutOfService = OutOfService
        self.Mileage = Mileage
        self.LastMaintenanceDate = LastMaintenanceDate
        self.InServiceDate = InServiceDate or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Employee(object):
    def __init__(self, ID = None, Firstname: str = None, Lastname: str = None, Role: str = None, Username: str = None, Password = None, IsTempPwd: int = None):
        self.ID = ID
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Role = Role
        self.Username = Username
        self.Password = Password
        self.IsTempPwd = IsTempPwd

class ScooterBrands(Enum):
    Vespa = "Vespa"
    Yamaha = "Yamaha"
    Honda = "Honda"
    SegwayNinebot = "Segway-Ninebot"   
    Xiaomi = "Xiaomi"

class VespaModels(Enum):
    VespaPrimavera50150 = "Vespa Primavera 50 / 150"
    VespaGTS300 = "Vespa GTS 300"
    VespaSprint50150 = "Vespa Sprint 50 / 150"
    VespaElettrica = "Vespa Elettrica"
    VespaLX125 = "Vespa LX 125"

class YamahaModels(Enum):
    YamahaNMAX155 = "Yamaha NMAX 155"
    YamahaAerox155 = "Yamaha Aerox 155"
    YamahaXMAX300 = "Yamaha XMAX 300"
    YamahaZuma125 = "Yamaha Zuma 125"
    YamahaDelight125 = "Yamaha Delight 125"

class HondaModels(Enum):
    HondaPCX160 = "Honda PCX 160"
    HondaMetropolitan = "Honda Metropolitan"
    HondaADV150 = "Honda ADV150"
    HondaDio = "Honda Dio"
    HondaSH150i = "Honda SH150i"

class SegwayNinebotModels(Enum):
    NinebotKickScooterMAXG2 = "Ninebot KickScooter MAX G2"
    NinebotF40 = "Ninebot F40"
    NinebotE45 = "Ninebot E45"
    NinebotAirT15 = "Ninebot Air T15"
    NinebotGT2 = "Ninebot GT2"

class XiaomiModels(Enum):
    XiaomiMiElectricScooterPro2 = "Xiaomi Mi Electric Scooter Pro 2"
    XiaomiMiEssential = "Xiaomi Mi Essential"
    Xiaomi4Pro = "Xiaomi 4 Pro"
    Xiaomi1S = "Xiaomi 1S"
    XiaomiElectricScooter3Lite = "Xiaomi Electric Scooter 3 Lite"

class Cities(Enum):
    Amsterdam = "Amsterdam"
    Rotterdam = "Rotterdam"
    Utrecht = "Utrecht"
    Eindhoven = "Eindhoven"
    Groningen = "Groningen"
    DenHaag = "Den Haag"
    Tilburg = "Tilburg"
    Almere = "Almere"
    Nijmegen = "Nijmegen"
    Breda = "Breda"