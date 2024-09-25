import sqlite3
import bcrypt
from Types import Employee, Member
from EncryptionDecryption import EncryptorDecryptor
class DBService(object):
    def __init__(self):
        self.encryptorDecryptor = EncryptorDecryptor()        
        self.connection = sqlite3.connect("MMSDB.db")
        self.DBCursor = self.connection.cursor()

    def SetupDatabase(self):
         self.DBCursor.execute("""CREATE TABLE IF NOT EXISTS "Employees" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"Firstname"	BLOB NOT NULL,
	"Lastname"	BLOB NOT NULL,
	"Role"	BLOB NOT NULL,
	"Username"	BLOB NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
    "IsTempPwd" NUMERIC,
	PRIMARY KEY("ID" AUTOINCREMENT));""")
         self.DBCursor.execute("""CREATE TABLE IF NOT EXISTS "Members" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"UID"	BLOB NOT NULL UNIQUE,
	"Firstname"	BLOB NOT NULL,
	"Lastname"	BLOB NOT NULL,
	"Age"		BLOB NOT NULL,
	"Gender"	BLOB NOT NULL,
	"Weight"	BLOB NOT NULL,
	"StreetName"	BLOB NOT NULL,
	"HouseNumber"	BLOB NOT NULL,
	"ZipCode"		BLOB NOT NULL,
    "City"		BLOB NOT NULL,
	"Email"		BLOB NOT NULL,
	"PhoneNumber"	BLOB NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT));""")
         
    def AddSysAdmin(self, admin: Employee):
        self.DBCursor.execute("""INSERT INTO "Employees" ('Firstname', 'Lastname', 'Role', 'Username', 'Password') VALUES(?,?,?,?,?)""", 
                              (self.encryptorDecryptor.Encrypt(admin.Firstname), 
                               self.encryptorDecryptor.Encrypt(admin.Lastname), 
                               self.encryptorDecryptor.Encrypt(admin.Role), 
                               self.encryptorDecryptor.Encrypt(admin.Username), 
                               bcrypt.hashpw(admin.Password.encode('utf-8'), bcrypt.gensalt())))
        self.connection.commit()

    def GetAllSysAdmins(self):
        employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
        SystemAdmin = []        
        for em in employees:        
            if (self.encryptorDecryptor.Decrypt(em[3]) == 'SystemAdmin'):
                SystemAdmin.append(em)
        return SystemAdmin         

    def GetAllConsultants(self):
        employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
        consultants = []        
        for em in employees:        
            if (self.encryptorDecryptor.Decrypt(em[3]) == 'Consultant'):
                consultants.append(em)
        return consultants                                            

    def UpdateEmployee(self, newSysAdmin: Employee, ID: int):
        self.DBCursor.execute("""UPDATE Employees SET Firstname = ?, Lastname = ?, Role = ?, Username = ? WHERE ID = ? """, 
                              (self.encryptorDecryptor.Encrypt(newSysAdmin.Firstname), 
                               self.encryptorDecryptor.Encrypt(newSysAdmin.Lastname), 
                               self.encryptorDecryptor.Encrypt(newSysAdmin.Role), 
                               self.encryptorDecryptor.Encrypt(newSysAdmin.Username), 
                               ID))
        self.connection.commit()

    def RemoveEmployee(self, ID: int):
        self.DBCursor.execute("""DELETE FROM Employees WHERE ID = ?""", (ID,))
        self.connection.commit()

    def AddNewMember(self, newMember: Member):
      self.DBCursor.execute("""INSERT INTO "Members" ('UID', 'Firstname', 'Lastname', 'Age', 'Gender', 'Weight', 'StreetName', 'HouseNumber', 'ZipCode', 'City', 'Email', 'PhoneNumber') VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
      (newMember.UID, 
       self.encryptorDecryptor.Encrypt(newMember.Firstname), 
       self.encryptorDecryptor.Encrypt(newMember.Lastname), 
       self.encryptorDecryptor.Encrypt(newMember.Age), 
       self.encryptorDecryptor.Encrypt(newMember.Gender), 
       self.encryptorDecryptor.Encrypt(newMember.Weight), 
       self.encryptorDecryptor.Encrypt(newMember.Address.StreetName), 
       self.encryptorDecryptor.Encrypt(newMember.Address.HouseNumber), 
       self.encryptorDecryptor.Encrypt(newMember.Address.ZipCode), 
       self.encryptorDecryptor.Encrypt(newMember.Address.City), 
       self.encryptorDecryptor.Encrypt(newMember.Email), 
       self.encryptorDecryptor.Encrypt(newMember.PhoneNumber)))
      self.connection.commit()

    def GetAllMembers(self):
        return self.DBCursor.execute("""SELECT * FROM Members""").fetchall()

    def UpdateMember(self, newMember: Member, UID: str):
        allMembers = self.DBCursor.execute("""SELECT * FROM Members""").fetchall()
        self.DBCursor.execute("""UPDATE Members SET Firstname = ?, Lastname = ?, Age = ?, Gender = ?, Weight = ?, StreetName = ?, HouseNumber = ?, ZipCode = ?, City = ?, Email = ?, PhoneNumber = ? WHERE UID = ?""",
        (self.encryptorDecryptor.Encrypt(newMember.Firstname), 
         self.encryptorDecryptor.Encrypt(newMember.Lastname), 
         self.encryptorDecryptor.Encrypt(newMember.Age), 
         self.encryptorDecryptor.Encrypt(newMember.Gender), 
         self.encryptorDecryptor.Encrypt(newMember.Weight), 
         self.encryptorDecryptor.Encrypt(newMember.Address.StreetName), 
         self.encryptorDecryptor.Encrypt(newMember.Address.HouseNumber), 
         self.encryptorDecryptor.Encrypt(newMember.Address.ZipCode), 
         self.encryptorDecryptor.Encrypt(newMember.Address.City), 
         self.encryptorDecryptor.Encrypt(newMember.Email), 
         self.encryptorDecryptor.Encrypt(newMember.PhoneNumber), 
         UID))
        self.connection.commit()        

    def RemoveMember(self, UID):
        self.DBCursor.execute("""DELETE FROM Members WHERE UID = ?""", (self.encryptorDecryptor.Encrypt(UID),))
        self.connection.commit()

    def UpdatePassword(self, pwd: str, ID: int, IsTempPwd: int = 1):
        self.DBCursor.execute("""UPDATE Employees SET Password = ?, IsTempPwd = ? WHERE ID = ?""", (bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()), IsTempPwd, ID))
        self.connection.commit()

    def GetPassword(self, ID: int):
        return self.DBCursor.execute("""SELECT Password FROM Employees WHERE ID = ?""", (ID,)).fetchall()               

    def Login(self, username: str, password: str):
       employees = self.DBCursor.execute("""SELECT * FROM Employees""").fetchall()
       for em in employees:           
            if (self.encryptorDecryptor.Decrypt(em[4]) == username and bcrypt.checkpw(password.encode('utf-8'), em[5])):
               return [em]