import sqlite3
import string
from datetime import datetime

import bcrypt

from EncryptionDecryption import EncryptorDecryptor
from Types import Employee, Scooter, Traveller


class DBService:
    def __init__(self):
        self.encryptorDecryptor = EncryptorDecryptor()
        self.connection = sqlite3.connect("UrbanMobility.db")
        self.DBCursor = self.connection.cursor()
        self.SetupDatabase()

    def SetupDatabase(self):
        self.DBCursor.execute("""
            CREATE TABLE IF NOT EXISTS Travellers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                Firstname BLOB NOT NULL,
                Lastname BLOB NOT NULL,
                Birthday BLOB NOT NULL,
                Gender BLOB NOT NULL,
                StreetName BLOB NOT NULL,
                HouseNumber BLOB NOT NULL,
                ZipCode BLOB NOT NULL,
                City BLOB NOT NULL,
                Email BLOB NOT NULL,
                PhoneNumber BLOB NOT NULL,
                DrivingLicenseNumber BLOB NOT NULL,
                RegistrationDate BLOB NOT NULL
            );
        """)

        self.DBCursor.execute("""CREATE TABLE IF NOT EXISTS "Employees" (
	    "ID"	INTEGER NOT NULL UNIQUE,
	    "Firstname"	BLOB NOT NULL,
	    "Lastname"	BLOB NOT NULL,
	    "Role"	BLOB NOT NULL,
	    "Username"	BLOB NOT NULL UNIQUE,
	    "Password"	TEXT NOT NULL,
        "IsTempPwd" NUMERIC,
	    PRIMARY KEY("ID" AUTOINCREMENT));""")

        self.DBCursor.execute("""
            CREATE TABLE IF NOT EXISTS Scooters (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Brand BLOB NOT NULL,
                Model BLOB NOT NULL,
                SerialNumber BLOB NOT NULL UNIQUE,
                TopSpeed BLOB NOT NULL,
                BatteryCapacity BLOB NOT NULL,
                StateOfCharge BLOB NOT NULL,
                TargetRangeMin BLOB NOT NULL,
                TargetRangeMax BLOB NOT NULL,
                LocationLat BLOB NOT NULL,
                LocationLong BLOB NOT NULL,
                OutOfService BLOB NOT NULL,
                Mileage BLOB NOT NULL,
                LastMaintenanceDate BLOB NOT NULL,
                InServiceDate BLOB NOT NULL
            );
        """)

        self.DBCursor.execute("""
            CREATE TABLE IF NOT EXISTS Backups (
             ID INTEGER PRIMARY KEY AUTOINCREMENT,
             BackupDate BLOB NOT NULL,
             RestoreCode TEXT,
             SystemAdmin ID,
             FOREIGN KEY (SystemAdmin) REFERENCES Employees(ID)
            )
        """)

        self.connection.commit()

    # ========== Backup Methods =============

    def AddBackup(self, date: str):
        self.DBCursor.execute("""
            INSERT INTO Backups (BackupDate) VALUES (?)""", (date))
        self.connection.commit()

    def AddBackupWithCode(self, date: str, code: str, SystemAdmin: int):
        self.DBCursor.execute("""
            INSERT INTO Backups (BackupDate, RestoreCode, SystemAdmin) VALUES (?,?,?)""", (date, code, SystemAdmin))
        self.connection.commit()

    def RemoveBackup(self, ID: int):
        self.DBCursor.execute("DELETE FROM Backups WHERE ID=?", (ID,))
        self.connection.commit()

    def AddOneTimeCodeToBackup(self, code: str, SystemAdmin: int, ID: int):
        self.DBCursor.execute("UPDATE Backups SET RestoreCode=?, SystemAdmin=? WHERE ID=?", (code, SystemAdmin, ID))
        self.connection.commit()

    def GetAllBackups(self):
        return self.DBCursor.execute("SELECT * FROM Backups").fetchall()

    def GetAllBackupsBySysAdmin(self, sysadmin: int):
        return self.DBCursor.execute("SELECT * FROM Backups WHERE SystemAdmin=?", (sysadmin,)).fetchall()


    # ========== Traveller Methods ==========

    def AddTraveller(self, traveller: Traveller):
        self.DBCursor.execute("""
            INSERT INTO Travellers (Firstname, Lastname, Birthday, Gender, StreetName, HouseNumber, ZipCode, City, Email, PhoneNumber, DrivingLicenseNumber, RegistrationDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (self.encryptorDecryptor.Encrypt(traveller.Firstname),
             self.encryptorDecryptor.Encrypt(traveller.Lastname),
             self.encryptorDecryptor.Encrypt(traveller.Birthday),
             self.encryptorDecryptor.Encrypt(traveller.Gender),
             self.encryptorDecryptor.Encrypt(traveller.StreetName),
             self.encryptorDecryptor.Encrypt(traveller.HouseNumber),
             self.encryptorDecryptor.Encrypt(traveller.ZipCode),
             self.encryptorDecryptor.Encrypt(traveller.City),
             self.encryptorDecryptor.Encrypt(traveller.Email),
             self.encryptorDecryptor.Encrypt(traveller.PhoneNumber),
             self.encryptorDecryptor.Encrypt(traveller.DrivingLicenseNumber),
             self.encryptorDecryptor.Encrypt(traveller.RegistrationDate))
        )
        self.connection.commit()

    def GetAllTravellers(self):
        return self.DBCursor.execute("SELECT * FROM Travellers").fetchall()

    def UpdateTraveller(self, traveller: Traveller, CustomerID: int):
        self.DBCursor.execute("""
            UPDATE Travellers SET Firstname=?, Lastname=?, Birthday=?, Gender=?, StreetName=?, HouseNumber=?, ZipCode=?, City=?, Email=?, PhoneNumber=?, DrivingLicenseNumber=?
            WHERE CustomerID=?""",
            (self.encryptorDecryptor.Encrypt(traveller.Firstname),
             self.encryptorDecryptor.Encrypt(traveller.Lastname),
             self.encryptorDecryptor.Encrypt(traveller.Birthday),
             self.encryptorDecryptor.Encrypt(traveller.Gender),
             self.encryptorDecryptor.Encrypt(traveller.StreetName),
             self.encryptorDecryptor.Encrypt(traveller.HouseNumber),
             self.encryptorDecryptor.Encrypt(traveller.ZipCode),
             self.encryptorDecryptor.Encrypt(traveller.City),
             self.encryptorDecryptor.Encrypt(traveller.Email),
             self.encryptorDecryptor.Encrypt(traveller.PhoneNumber),
             self.encryptorDecryptor.Encrypt(traveller.DrivingLicenseNumber),
             CustomerID)
        )
        self.connection.commit()

    def DeleteTraveller(self, CustomerID: int):
        self.DBCursor.execute("DELETE FROM Travellers WHERE CustomerID=?", (CustomerID,))
        self.connection.commit()

    # ========== Scooter Methods ==========

    def AddScooter(self, scooter: Scooter):
        self.DBCursor.execute("""
            INSERT INTO Scooters (Brand, Model, SerialNumber, TopSpeed, BatteryCapacity, StateOfCharge, TargetRangeMin, TargetRangeMax, LocationLat, LocationLong, OutOfService, Mileage, LastMaintenanceDate, InServiceDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (self.encryptorDecryptor.Encrypt(scooter.Brand),
             self.encryptorDecryptor.Encrypt(scooter.Model),
             self.encryptorDecryptor.Encrypt(scooter.SerialNumber),
             self.encryptorDecryptor.Encrypt(scooter.TopSpeed),
             self.encryptorDecryptor.Encrypt(scooter.BatteryCapacity),
             self.encryptorDecryptor.Encrypt(scooter.StateOfCharge),
             self.encryptorDecryptor.Encrypt(scooter.TargetRangeMin),
             self.encryptorDecryptor.Encrypt(scooter.TargetRangeMax),
             self.encryptorDecryptor.Encrypt(scooter.LocationLat),
             self.encryptorDecryptor.Encrypt(scooter.LocationLong),
             self.encryptorDecryptor.Encrypt(int(scooter.OutOfService)),
             self.encryptorDecryptor.Encrypt(scooter.Mileage),
             self.encryptorDecryptor.Encrypt(scooter.LastMaintenanceDate),
             self.encryptorDecryptor.Encrypt(scooter.InServiceDate))
        )
        self.connection.commit()

    def GetAllScooters(self):
        return self.DBCursor.execute("SELECT * FROM Scooters").fetchall()

    def UpdateScooter(self, scooter: Scooter, ID: int):
        self.DBCursor.execute("""
            UPDATE Scooters SET Brand=?, Model=?, SerialNumber=?, TopSpeed=?, BatteryCapacity=?, StateOfCharge=?, TargetRangeMin=?, TargetRangeMax=?, LocationLat=?, LocationLong=?, OutOfService=?, Mileage=?, LastMaintenanceDate=?
            WHERE ID=?""",
            (self.encryptorDecryptor.Encrypt(scooter.Brand),
             self.encryptorDecryptor.Encrypt(scooter.Model),
             self.encryptorDecryptor.Encrypt(scooter.SerialNumber),
             self.encryptorDecryptor.Encrypt(scooter.TopSpeed),
             self.encryptorDecryptor.Encrypt(scooter.BatteryCapacity),
             self.encryptorDecryptor.Encrypt(scooter.StateOfCharge),
             self.encryptorDecryptor.Encrypt(scooter.TargetRangeMin),
             self.encryptorDecryptor.Encrypt(scooter.TargetRangeMax),
             self.encryptorDecryptor.Encrypt(scooter.LocationLat),
             self.encryptorDecryptor.Encrypt(scooter.LocationLong),
             self.encryptorDecryptor.Encrypt(int(scooter.OutOfService)),
             self.encryptorDecryptor.Encrypt(scooter.Mileage),
             self.encryptorDecryptor.Encrypt(scooter.LastMaintenanceDate),
             ID)
        )
        self.connection.commit()

    def DeleteScooter(self, ID: int):
        self.DBCursor.execute("DELETE FROM Scooters WHERE ID=?", (ID,))
        self.connection.commit()

    def UpdateEmployee(self, newSysAdmin: Employee, ID: int):
            self.DBCursor.execute("""UPDATE Employees SET Firstname = ?, Lastname = ?, Role = ?, Username = ? WHERE ID = ? """, 
                                  (self.encryptorDecryptor.Encrypt(newSysAdmin.Firstname), 
                                   self.encryptorDecryptor.Encrypt(newSysAdmin.Lastname), 
                                   self.encryptorDecryptor.Encrypt(newSysAdmin.Role), 
                                   self.encryptorDecryptor.Encrypt(newSysAdmin.Username), 
                                   ID))
            self.connection.commit()

    def UpdatePassword(self, pwd: str, ID: int, IsTempPwd: int = 1):
            self.DBCursor.execute("""UPDATE Employees SET Password = ?, IsTempPwd = ? WHERE ID = ?""", (bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()), IsTempPwd, ID))
            self.connection.commit()

    def AddEmployee(self, employee):
        self.DBCursor.execute("""
            INSERT INTO Employees (Firstname, Lastname, Role, Username, Password, IsTempPwd)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.encryptorDecryptor.Encrypt(employee.Firstname),
                self.encryptorDecryptor.Encrypt(employee.Lastname),
                self.encryptorDecryptor.Encrypt(employee.Role),
                self.encryptorDecryptor.Encrypt(employee.Username),
                employee.Password,
                employee.IsTempPwd
            )
        )
        self.connection.commit()

    def GetAllEmployees(self):
        return self.DBCursor.execute("SELECT * FROM Employees").fetchall()
        self.connection.commit()

    def GetAllSysAdmins(self):
        employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
        SystemAdmin = []
        for em in employees:
            if (self.encryptorDecryptor.Decrypt(em[3]) == 'SystemAdmin'):
                SystemAdmin.append(em)
        return SystemAdmin

    def GetAllServiceEngineers(self):
        employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
        ServiceEngineer = []
        for em in employees:
            if (self.encryptorDecryptor.Decrypt(em[3]) == 'ServiceEngineer'):
                ServiceEngineer.append(em)
        return ServiceEngineer

    def AddSysAdmin(self, admin: Employee):
            self.DBCursor.execute("""INSERT INTO "Employees" ('Firstname', 'Lastname', 'Role', 'Username', 'Password') VALUES(?,?,?,?,?)""", 
                                  (self.encryptorDecryptor.Encrypt(admin.Firstname), 
                                   self.encryptorDecryptor.Encrypt(admin.Lastname), 
                                   self.encryptorDecryptor.Encrypt(admin.Role), 
                                   self.encryptorDecryptor.Encrypt(admin.Username), 
                                   bcrypt.hashpw(admin.Password.encode('utf-8'), bcrypt.gensalt())))
            self.connection.commit()

    def RemoveEmployee(self, ID: int):
        self.DBCursor.execute("""DELETE FROM Employees WHERE ID = ?""", (ID,))
        self.connection.commit()

    def Login(self, username: str, password: str):
       employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
       for em in employees:           
            if (self.encryptorDecryptor.Decrypt(em[4]) == username and bcrypt.checkpw(password.encode('utf-8'), em[5])):
               return [em]

    def GetPassword(self, ID: int):
        return self.DBCursor.execute("""SELECT Password FROM Employees WHERE ID = ?""", (ID,)).fetchall()   
    def GetPassword(self, ID: int):
        return self.DBCursor.execute("""SELECT Password FROM Employees WHERE ID = ?""", (ID,)).fetchall()   
    def GetPassword(self, ID: int):
        return self.DBCursor.execute("""SELECT Password FROM Employees WHERE ID = ?""", (ID,)).fetchall()   