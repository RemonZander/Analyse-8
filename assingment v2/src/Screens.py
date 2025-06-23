import base64
import datetime
import getpass
import logging
import os
import shutil
from time import sleep
from zipfile import ZipFile

import bcrypt

from InputValidation import InputValidator
from screen import Screen
from Types import Employee, Scooter, Traveller


class LoginScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        print("Login into UrbanMobility Backed System")
        username = ""
        password = ""
        isLoggedIn = False
        tries = 0
        super_admin_hash = "$2a$12$Y7hj3sZvun3x1y.eCsLVv.SycGQ0QkJe1NVlLzOBTCjucPYMO/PqK"

        while isLoggedIn == False and tries < 3:
            usernameInput = input("username: ")
            username = usernameInput if InputValidator.IsValidUsername(usernameInput) else ""

            password = getpass.getpass("password: ")
            if (not InputValidator.IsValidPassword(password)):
                print("Login Failed, try again...")
                if (tries == 2):
                    self.Logger("", "login", f"username: {username} failed to login", "yes", logging.WARNING)
                else:
                    self.Logger("", "login", f"username: {username} failed to login", "no", logging.INFO)
                sleep(2)
                tries += 1
                continue
            
            if username == "super_admin" and bcrypt.checkpw(password.encode('utf-8'), super_admin_hash):
                self.LoggedInEmployee.Role = "SuperAdmin"
                self.LoggedInEmployee.Username = "super_admin"
                isLoggedIn = True
                self.Logger(self.LoggedInEmployee.Username, "login", "succesfull login", "no")
                return 1
            else:
                userTemp = self.DB.Login(username, password)
                if (userTemp == None):
                    print("Login Failed, try again...")
                    if (tries == 2):
                        self.Logger("", "login", f"username: {username} failed to login", "yes", logging.WARNING)
                    else:
                        self.Logger("", "login", f"username: {username} failed to login", "no", logging.INFO)
                    sleep(2)
                    tries += 1
                else:
                    self.LoggedInEmployee.Role = self.encryptorDecryptor.Decrypt(userTemp[0][3])
                    self.LoggedInEmployee.Username = self.encryptorDecryptor.Decrypt(userTemp[0][4])
                    self.LoggedInEmployee.ID = userTemp[0][0]
                    self.LoggedInEmployee.IsTempPwd = userTemp[0][6]
                    isLoggedIn = True
                    self.Logger(self.LoggedInEmployee.Username, "login", "succesfull login", "no")
                    return 1
        if (isLoggedIn == False):
            print("You have tried to login 3 times, the program will now exit")
            return -1

class HomeScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering home screen", "", "no")
        if (self.LoggedInEmployee.IsTempPwd == 1):
            print("You have a temporary password. You will be send to a new screen to reset your password...")
            sleep(1)
            return 9
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print("welcome super administrator\n\n")
            print("###################################################################")
            print("# [1] add new system administrator or service engineer            #")
            print("# [2] edit or remove a system administrator or Service Engineer   #")
            print("# [3] add new traveller                                           #")
            print("# [4] edit or remove a traveller                                  #")
            print("# [5] display list of users with their roles                      #")
            print("# [6] display list of travellers                                  #")
            print("# [7] reset Service Engineer password                             #")
            print("# [8] reset system admin password                                 #")
            print("# [9] manage backups                                              #")
            print("# [10] display log files                                          #")
            print("# [11] search traveller                                           #")
            print("# [12] add scooter                                                #")
            print("# [13] edit or remove scooter                                     #")
            print("# [14] display list of scooters                                   #")
            print("# [15] search scooter                                             #")
            print("# [16] exit program                                               #")
            print("###################################################################\n")
            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 16)): return 1
            
            if (int(choice) == 1):
                return 2
            elif (int(choice) == 2):
                return 3
            elif (int(choice) == 3):
                return 14
            elif (int(choice) == 4):
                return 15
            elif (int(choice) == 5):
                return 4
            elif (int(choice) == 6):
                return 17
            elif (int(choice) == 7):
                return 6
            elif (int(choice) == 8):
                return 7
            elif (int(choice) == 9):
                return 10
            elif (int(choice) == 10):
                return 8
            elif (int(choice) == 11):
                return 16
            elif (int(choice) == 12):
                return 12
            elif (int(choice) == 13):
                return 13
            elif (int(choice) == 14):
                return 5
            elif (int(choice) == 15):
                return 11
            else:
                return -1
        
        elif (self.LoggedInEmployee.Role == "SystemAdmin"):
            print("welcome system administrator\n\n")
            print("###################################################################")
            print("# [1] add new service engineer                                    #")
            print("# [2] edit or remove a system administrator or Service Engineer   #")
            print("# [3] add new traveller                                           #")
            print("# [4] edit or remove a traveller                                  #")
            print("# [5] display list of users with their roles                      #")
            print("# [6] display list of traveller                                   #")
            print("# [7] reset Service Engineer password                             #")
            print("# [8] manage backups                                              #")
            print("# [9] display log files                                           #")
            print("# [10] search traveller                                           #")
            print("# [11] update own password                                        #")
            print("# [12] add scooter                                                #")
            print("# [13] edit or remove scooter                                     #")
            print("# [14] display list of scooters                                   #")
            print("# [15] search scooter                                             #")
            print("# [16] exit program                                               #")
            print("###################################################################\n")
            choice =input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 16)): return 1
            
            if (int(choice) == 1):
                return 2
            elif (int(choice) == 2):
                return 3
            elif (int(choice) == 3):
                return 14
            elif (int(choice) == 4):
                return 15
            elif (int(choice) == 5):
                return 4
            elif (int(choice) == 6):
                return 17
            elif (int(choice) == 7):
                return 6
            elif (int(choice) == 8):
                return 10
            elif (int(choice) == 9):
                return 8
            elif (int(choice) == 10):
                return 16
            elif (int(choice) == 11):
                return 9
            elif (int(choice) == 12):
                return 12
            elif (int(choice) == 13):
                return 13
            elif (int(choice) == 14):
                return 5
            elif (int(choice) == 15):
                return 11
            else:
                return -1
        else:
            print("welcome Service Engineer\n\n")
            print("####################################")
            print("# [1] update own password          #")
            print("# [2] update scooter               #")
            print("# [3] display list of scooters     #")
            print("# [4] search scooters              #")
            print("# [5] exit program                 #")
            print("####################################\n")
            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 5)): return 1
            
            if (int(choice) == 1):
                return 9
            elif (int(choice) == 2):
                return 13
            elif (int(choice) == 3):
                return 5
            elif (int(choice) == 4):
                return 11
            elif (int(choice) == 5):
                return -1
        return 1

class AddSysAdminOrServiceEngineerScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering add sys admin / Service Engineer screen", "", "no")
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print("Fill in the information for the new system administrator or Service Engineer:\n")
        else:
            print("Fill in the information for the new Service Engineer:\n")
        newSysAdmin = Employee()

        FirstNameInput = input("First Name: ")
        if (not InputValidator.IsValidName(FirstNameInput)):
            print("Invalid first name. Please try again.")
            sleep(2)
            return 2
        newSysAdmin.Firstname = FirstNameInput

        LastNameInput = input("Last Name: ")
        if (not InputValidator.IsValidName(LastNameInput)):
            print("Invalid last name. Please try again.")
            sleep(2)
            return 2
        newSysAdmin.Lastname = LastNameInput

        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print()
            print("Choose Role: ")
            print("[1] system admin")
            print("[2] Service Engineer")
            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 2)): return 2
            if (int(choice) == 1):
                newSysAdmin.Role = "SystemAdmin"
            elif (int(choice) == 2):
                newSysAdmin.Role = "ServiceEngineer"
        else:
            newSysAdmin.Role = "ServiceEngineer"
        usernameInput = input("Username (8-10 characters, must start with a letter): ")
        if (not InputValidator.IsValidUsername(usernameInput)):
            print("Invalid username. Please try again.")
            sleep(2)
            return 2
        newSysAdmin.Username = usernameInput

        passwordInput = input("Password (Minimum of 12 characters, at least one lower case letter, one upper case letter, one digit and one special character): ")
        if (not InputValidator.IsValidPassword(passwordInput)):
            print("Invalid password. Please try again.")
            sleep(2)
            return 2
        newSysAdmin.Password = passwordInput

        self.DB.AddSysAdmin(newSysAdmin)
        self.Logger(self.LoggedInEmployee.Username, f"saving new {'sys admin' if newSysAdmin.Role == 'SystemAdmin' else 'ServiceEngineer'} {newSysAdmin.Username}", "", "no")
        print(f"Saved {'system admin' if newSysAdmin.Role == 'SystemAdmin' else 'ServiceEngineer'}. Returning to main menu...")
        sleep(1)
        return 1

class EditSysAdminOrServiceEngineerScreen(Screen):
    def __init__(self):
        pass
            
    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering edit or delete sys admin / Service Engineer screen", "", "no")
        employees = []
        print("[1] Edit system admin")
        print("[2] Edit Service Engineer")
        choice4 = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice4, 2)): return 3

        if (choice4 == "1"):
            employees =  self.DB.GetAllSysAdmins()
        else:
            employees = self.DB.GetAllServiceEngineers()
        print("----------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
        print("----------------------------------------------------------------------------------")
        for a in range(len(employees)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("----------------------------------------------------------------------------------")
            
        choice = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice, len(employees))): return 3
        print("\n\n")
        print("[1] edit user")
        print("[2] remove user")
        choice2 = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice2, 2) ): return 3
        if (choice2 == "1"):
            UpdatedEmployee = Employee()
            print(f"Current firstname: {self.encryptorDecryptor.Decrypt(employees[int(choice)][1])}")
            FirstNameInput = input("First Name: ")
            if (not InputValidator.IsValidName(FirstNameInput)):
                print("Invalid first name. Please try again.")
                sleep(2)
                return 3
            UpdatedEmployee.Firstname = FirstNameInput
            
            print(f"Current lastname: {self.encryptorDecryptor.Decrypt(employees[int(choice)][2])}")
            LastNameInput = input("Last Name: ")
            if (not InputValidator.IsValidName(LastNameInput)):
                print("Invalid last name. Please try again.")
                sleep(2)
                return 3
            UpdatedEmployee.Lastname = LastNameInput
            
            if (self.LoggedInEmployee.Role == "SuperAdmin"):
                print("Choose Role: ")
                print("[1] system admin")
                print("[2] Service Engineer")
                choice3 = input("Make a choice: ")
                if (not InputValidator.IsValidChoiceInput(choice3, 2)): return 3
                if (choice3 == "1"):
                    UpdatedEmployee.Role = "SystemAdmin"
                elif (choice3 == "2"):
                    UpdatedEmployee.Role = "ServiceEngineer"
            else:
                UpdatedEmployee.Role = self.encryptorDecryptor.Decrypt(employees[int(choice)][3])
            print(f"Current username: {self.encryptorDecryptor.Decrypt(employees[int(choice)][4])}")
            
            usernameInput = input("Username (8-10 characters, must start with a letter): ")
            if (not InputValidator.IsValidUsername(usernameInput)):
                print("Invalid username. Please try again.")
                sleep(2)
                return 3
            UpdatedEmployee.Username = usernameInput
            self.DB.UpdateEmployee(UpdatedEmployee, employees[int(choice)][0])
            self.Logger(self.LoggedInEmployee.Username, f"edited {'sys admin' if UpdatedEmployee.Role == 'SystemAdmin' else 'ServiceEngineer'} {UpdatedEmployee.Username}", "", "no")
            print(f"Updated {'system admin' if choice4 == 1 else 'Service Engineer'}. Returning to home screen...")
            sleep(1)
        elif (choice2 == "2"):
            self.DB.RemoveEmployee(employees[int(choice)][0])
            self.Logger(self.LoggedInEmployee.Username, f"removed {'sys admin' if self.encryptorDecryptor.Decrypt(employees[int(choice)][3]) == 'SystemAdmin' else 'Service Engineer'} {self.encryptorDecryptor.Decrypt(employees[int(choice)][4])}", "", "no")
            print(f"Removed {'system admin' if choice4 == 1 else 'Service Engineer'}. Returning to home screen...")
            sleep(1)
        return 1

class ShowEmployees(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering show employee screen", "", "no")
        employees = self.DB.GetAllEmployees()
        print("-------------------------------------------------------------------------")
        print(f"| {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
        print("-------------------------------------------------------------------------")
        for a in range(len(employees)):
            print(f"| {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("-------------------------------------------------------------------------")
        print("\n")
        print("Press [1] to return to home screen: ")
        choice = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice, 2)): return 1
        return 1

class ShowScootersScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering show scooter screen", "", "no")
        encryptedscooters = self.DB.GetAllScooters()
        decryptedscooters: list[Scooter] = []
        for eSCO in encryptedscooters:
            tempScooter = Scooter(
                self.encryptorDecryptor.Decrypt(eSCO[1]),
                self.encryptorDecryptor.Decrypt(eSCO[2]),
                self.encryptorDecryptor.Decrypt(eSCO[3]),
                self.encryptorDecryptor.Decrypt(eSCO[4]),
                self.encryptorDecryptor.Decrypt(eSCO[5]),
                self.encryptorDecryptor.Decrypt(eSCO[6]),
                self.encryptorDecryptor.Decrypt(eSCO[7]),
                self.encryptorDecryptor.Decrypt(eSCO[8]),
                self.encryptorDecryptor.Decrypt(eSCO[9]),
                self.encryptorDecryptor.Decrypt(eSCO[10]),
                self.encryptorDecryptor.Decrypt(eSCO[11]),
                self.encryptorDecryptor.Decrypt(eSCO[12]),
                self.encryptorDecryptor.Decrypt(eSCO[13]),
                self.encryptorDecryptor.Decrypt(eSCO[14])
                )
            decryptedscooters.append(tempScooter)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"{self.RepeatString(' ', 25, 'brand')} | {self.RepeatString(' ', 25, 'model')} | {self.RepeatString(' ', 25, 'Serial number')} | {self.RepeatString(' ', 25, 'Top speed')} | {self.RepeatString(' ', 25, 'Battery Capacity')} | {self.RepeatString(' ', 25, 'State of Charge')} | {self.RepeatString(' ', 25, 'Target-range SoC')} | {self.RepeatString(' ', 25, 'Location')} | {self.RepeatString(' ', 25, 'Out-of-service status')} | {self.RepeatString(' ', 25, 'Mileage')} | {self.RepeatString(' ', 25, 'Last maintenance date')} |")
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(decryptedscooters)):
            print(f"""{self.RepeatString(' ', 25, decryptedscooters[a].Brand)} | {self.RepeatString(' ', 25, decryptedscooters[a].Model)} | {self.RepeatString(' ', 25, decryptedscooters[a].SerialNumber)} | {self.RepeatString(' ', 25, decryptedscooters[a].TopSpeed)} | {self.RepeatString(' ', 25, decryptedscooters[a].BatteryCapacity)} | {self.RepeatString(' ', 25, decryptedscooters[a].StateOfCharge)} | {self.RepeatString(' ', 25, f"{decryptedscooters[a].TargetRangeMin}-{decryptedscooters[a].TargetRangeMax}")} | {self.RepeatString(' ', 25, f"{decryptedscooters[a].LocationLat}-{decryptedscooters[a].LocationLong}")}  | {self.RepeatString(' ', 25, decryptedscooters[a].OutOfService)} | {self.RepeatString(' ', 25, decryptedscooters[a].Mileage)} | {self.RepeatString(' ', 25, decryptedscooters[a].LastMaintenanceDate)} |""")
            print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("\n")
        choice = input("Press [1] to return to home screen: ")
        if (not InputValidator.IsValidChoiceInput(choice, 1)): return 1
        return 1

class ResetServiceEngineerScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering reset Service Engineer password screen", "", "no")
        employees =  self.DB.GetAllServiceEngineers()
        print("----------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
        print("----------------------------------------------------------------------------------")
        for a in range(len(employees)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("----------------------------------------------------------------------------------")
            
        choice = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice, len(employees)) ): return 6
        print("\n\n")
        newPasswordInput = input("Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
        if (not InputValidator.IsValidPassword(newPasswordInput)):
            print("Invalid password. Please try again.")
            return 8
        newPassword = newPasswordInput
        
        newPassword2Input = input("Retype password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
        if (not InputValidator.IsValidPassword(newPassword2Input)):
            print("Invalid password. Please try again.")
            return 6
        newPassword2 = newPassword2Input
        
        if (newPassword == newPassword2):
            self.DB.UpdatePassword(newPassword, employees[a][0])
            print("Password Updated. Returning to home screen...")
            self.Logger(self.LoggedInEmployee.Username, f"reset password for Service Engineer: {self.encryptorDecryptor.Decrypt(employees[a][4])}", "", "no")
            sleep(1)
            return 1

class ResetSysAdminPassScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering reset sys admin password screen", "", "no")
        employees =  self.DB.GetAllSysAdmins()
        print("----------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
        print("----------------------------------------------------------------------------------")
        for a in range(len(employees)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("----------------------------------------------------------------------------------")
            
        choice = input("Make a choice: ")
        if ( not InputValidator.IsValidChoiceInput(choice, len(employees)) ): return 7
        print("\n\n")
        newPasswordInput = input("Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
        if (not InputValidator.IsValidPassword(newPasswordInput)):
            print("Invalid password. Please try again.")
            return 7
        newPassword = newPasswordInput
        
        newPassword2Input = input("Retype password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
        if (not InputValidator.IsValidPassword(newPassword2Input)):
            print("Invalid password. Please try again.")
            return 7
        newPassword2 = newPassword2Input
        
        if (newPassword == newPassword2):
            self.DB.UpdatePassword(newPassword, employees[a][0])
            print("Password Updated. Returning to home screen...")
            self.Logger(self.LoggedInEmployee.Username, f"reset password for sys admin: {self.encryptorDecryptor.Decrypt(employees[a][4])}", "", "no")             
            sleep(1)
            return 1

class ReadLogsScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "Reading logs", "", "no")
        files = os. listdir("./logs")
        for a in range(len(files)):
            print(f"[{a}] | Filename: {files[a]}")
        choice = input("Make a choice: ")
        if ( not InputValidator.IsValidChoiceInput(choice, len(files)) ): return 8
        print("\n")
        with open(f"./logs/{files[int(choice)]}", "rb") as file:
            for line in file:
                try:
                    print(base64.b64decode(line).rstrip()[:base64.b64decode(line).rstrip().rfind("] ".encode('utf-8')) + 2].decode('utf-8') + self.encryptorDecryptor.Decrypt(base64.b64decode(line).rstrip()[base64.b64decode(line).rstrip().rfind('] '.encode('utf-8')) + 2:]))
                except:
                    pass
        print("\n")
        print("Press [1] to return to home screen: ")
        choice = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice, 1)): return 1
        return 1

class UpdatePasswordScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "Resetting own password", "", "no")
        oldpwd = self.DB.GetPassword(self.LoggedInEmployee.ID)[0][0]
        currentPassword = input("Current password: ")
        if (not InputValidator.IsValidPassword(currentPassword)):
                print("Invalid password. Please try again.")
                return 9
        if (bcrypt.checkpw(currentPassword.encode('utf-8'), oldpwd)):
            newPasswordInput = input("Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
            if (not InputValidator.IsValidPassword(newPasswordInput)):
                print("Invalid password. Please try again.")
                return 9
            newPassword = newPasswordInput
            
            newPassword2Input = input("Retype password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ")
            if (not InputValidator.IsValidPassword(newPassword2Input)):
                print("Invalid password. Please try again.")
                return 9
            newPassword2 = newPassword2Input

            if (newPassword == newPassword2):
                self.DB.UpdatePassword(newPassword, self.LoggedInEmployee.ID, 0)
                self.LoggedInEmployee.IsTempPwd = 0
                print("Password Updated. Returning to home screen...")
                sleep(1)
                return 1

class ManageBackups(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering backup screen", "", "no")
        print("[1] restore a backup")
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print("[2] make a backup")
            print("[3] Add one time code to existing backup")

            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 3)): return 10
        else:
            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, 1)): return 10

        if (int(choice) == 1):
            backups = []
            if (self.LoggedInEmployee.Role == "SystemAdmin"):
                backups = self.DB.GetAllBackupsBySysAdmin(self.LoggedInEmployee.ID)
            elif (self.LoggedInEmployee.Role == "SuperAdmin"):
                backups = self.DB.GetAllBackups()
            else:
                return 1

            if (len(backups) == 0):
                print("There are no backups to restore. Going back to home...")
                sleep(2)
                return 1
            
            for a in range(len(backups)):
                print(f"[{a}] | Backup: {backups[a][1]}")
            choice = input("Make a choice: ")    #input checking!!!
            if ( not InputValidator.IsValidChoiceInput(choice, len(backups)) ): return 10
            try:
                shutil.rmtree('./logs')
            except :
                pass
            shutil.unpack_archive(f"./backups/backup {backups[int(choice)][1]}.zip", './')
            if (self.LoggedInEmployee.Role == "SystemAdmin"):
                self.DB.AddOneTimeCodeToBackup("", None, backups[int(choice)][0])
            self.Logger(self.LoggedInEmployee.Username, f"Restoring backup: {backups[int(choice)][1]}", "", "no")
            print("Backup has been restored. The program will now shut down...")
            sleep(2)
            return -1
        elif (int(choice) == 2):
            if (self.LoggedInEmployee.Role == "SystemAdmin"): return 10
            employees =  self.DB.GetAllSysAdmins()
            print("----------------------------------------------------------------------------------")
            print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
            print("----------------------------------------------------------------------------------")
            for a in range(len(employees)):
                print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
                print("----------------------------------------------------------------------------------")

            choice = input("Select a system admin to give access to use this backup or press enter to skip: ")
            if (not InputValidator.IsValidChoiceInput(choice, len(employees) + 1)): return 10

            onetimecode = ""
            if (choice != ""):
                onetimecode = input("Fill in the onetime code for the system admin: ")
                self.Logger(self.LoggedInEmployee.Username, f"added a onetime code for the new backup. systemadmin with access: {self.encryptorDecryptor.Decrypt(employees[int(choice)][1])}  {self.encryptorDecryptor.Decrypt(employees[int(choice)][2])}", "", "no")
            dateOfBackup = datetime.datetime.now().strftime('%H-%M-%S %d-%m-%Y')
            filename = f"./backups/backup {dateOfBackup}"
            shutil.make_archive(filename, format='zip', root_dir='.', base_dir='./logs')
            with ZipFile(filename + ".zip",'a') as zip:
                zip.write('./UrbanMobility.db')
                zip.write('./keys/private_key.pem')
                zip.write('./keys/public_key.pem')
            self.Logger(self.LoggedInEmployee.Username, f"Creating backup: {filename}", "", "no")
            if (choice != "" and onetimecode != ""):
                self.DB.AddBackupWithCode(dateOfBackup, onetimecode, employees[int(choice)][0])
            else:
                self.DB.AddBackup("", dateOfBackup)
            print(f"Backup: {filename} has been made. Returning to home screen...")
            sleep(2)
            return 1
        else:
            backups = self.DB.GetAllBackups()
            for a in range(len(backups)):
                print(f"[{a}] | Backup: {backups[a].BackupDate}")
            choice = input("Make a choice: ")
            if (not InputValidator.IsValidChoiceInput(choice, len(backups)) ): return 10
            employees =  self.DB.GetAllSysAdmins()
            print("----------------------------------------------------------------------------------")
            print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")
            print("----------------------------------------------------------------------------------")
            for a in range(len(employees)):
                print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
                print("----------------------------------------------------------------------------------")

            choice = input("Select a system admin to give access to use this backup")
            if (not InputValidator.IsValidChoiceInput(choice, len(employees))): return 10
            oneTimeCode = input("One time code: ")
            if (not InputValidator.IsValidBackupCode(oneTimeCode)):
                print("Invalid one time code. Please try again.")
                sleep(2)
                return 10
            self.DB.AddOneTimeCodeToBackup(oneTimeCode, choice, backups[int(choice)][0])
            print("Added onetime code to the backup. Retuning to homescreen...")
            sleep(2)
            return 1

class SearchScooterScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering search scoorter schreen", "", "no")
        encryptedscooters = self.DB.GetAllScooters()
        decryptedscooters: list[Scooter] = []
        hits = []
        for eSCO in encryptedscooters:
            tempScooter = Scooter(
                self.encryptorDecryptor.Decrypt(eSCO[1]),
                self.encryptorDecryptor.Decrypt(eSCO[2]),
                self.encryptorDecryptor.Decrypt(eSCO[3]),
                self.encryptorDecryptor.Decrypt(eSCO[4]),
                self.encryptorDecryptor.Decrypt(eSCO[5]),
                self.encryptorDecryptor.Decrypt(eSCO[6]),
                self.encryptorDecryptor.Decrypt(eSCO[7]),
                self.encryptorDecryptor.Decrypt(eSCO[8]),
                self.encryptorDecryptor.Decrypt(eSCO[9]),
                self.encryptorDecryptor.Decrypt(eSCO[10]),
                self.encryptorDecryptor.Decrypt(eSCO[11]),
                self.encryptorDecryptor.Decrypt(eSCO[12]),
                self.encryptorDecryptor.Decrypt(eSCO[13]),
                self.encryptorDecryptor.Decrypt(eSCO[14])
                )
            decryptedscooters.append(tempScooter)
        
        searchString = input("Search string: ")  #input checking!!!
        if (not InputValidator.IsValidSearchInput(searchString)): return 17
        for dSCO in decryptedscooters:
            if (searchString in dSCO.BatteryCapacity or searchString in dSCO.Brand.lower() or searchString in dSCO.InServiceDate.lower() or searchString in str(dSCO.LocationLat) or searchString in str(dSCO.LocationLong)
            or searchString in str(dSCO.Mileage) or searchString in dSCO.Model.lower() or searchString in dSCO.SerialNumber.lower() or searchString in dSCO.OutOfService
            or searchString in dSCO.StateOfCharge or searchString in dSCO.TargetRangeMax or searchString in dSCO.TargetRangeMin or searchString in dSCO.TopSpeed):  
                hits.append(dSCO)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"{self.RepeatString(' ', 25, 'brand')} | {self.RepeatString(' ', 25, 'model')} | {self.RepeatString(' ', 25, 'Serial number')} | {self.RepeatString(' ', 25, 'Top speed')} | {self.RepeatString(' ', 25, 'Battery Capacity')} | {self.RepeatString(' ', 25, 'State of Charge')} | {self.RepeatString(' ', 25, 'Target-range SoC')} | {self.RepeatString(' ', 25, 'Location')} | {self.RepeatString(' ', 25, 'Out-of-service status')} | {self.RepeatString(' ', 25, 'Mileage')} | {self.RepeatString(' ', 25, 'Last maintenance date')} |")
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(hits)):
            print(f"""{self.RepeatString(' ', 25, hits[a].Brand)} | {self.RepeatString(' ', 25, hits[a].Model)} | {self.RepeatString(' ', 25, hits[a].SerialNumber)} | {self.RepeatString(' ', 25, hits[a].TopSpeed)} | {self.RepeatString(' ', 25, hits[a].StateOfCharge)} | {self.RepeatString(' ', 25, f"{hits[a].TargetRangeMin}-{hits[a].TargetRangeMax}")} | {self.RepeatString(' ', 25, f"{hits[a].LocationLat}-{hits[a].LocationLong}")}  | {self.RepeatString(' ', 25, hits[a].OutOfService)} | {self.RepeatString(' ', 25, hits[a].Mileage)} | {self.RepeatString(' ', 25, hits[a].LastMaintenanceDate)} |""")
            print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("\n")
        choice = input("Press [1] to return to home screen: ")
        if (not InputValidator.IsValidChoiceInput(choice, 1)): return 1
        return 1

class AddScooterScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering add new scooter screen", "", "no")
        print("Fill in the information for a new scooter \n")
        newScooter = Scooter()
        if (not self.AddOrEditScooter(newScooter)): return 12
        self.DB.AddScooter(newScooter)
        self.Logger(self.LoggedInEmployee.Username, "Added a new scooter", "", "no")
        print("Saved new scooter. Returning to home screen...")
        sleep(1)
        return 1

class EditOrRemoveScooter(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering edit or delete scooter screen", "", "no")
        encryptedscooters = self.DB.GetAllScooters()
        decryptedscooters = []
        for eSCO in encryptedscooters:
            tempScooter = Scooter(
                eSCO[0],
                self.encryptorDecryptor.Decrypt(eSCO[1]),
                self.encryptorDecryptor.Decrypt(eSCO[2]),
                self.encryptorDecryptor.Decrypt(eSCO[3]),
                self.encryptorDecryptor.Decrypt(eSCO[4]),
                self.encryptorDecryptor.Decrypt(eSCO[5]),
                self.encryptorDecryptor.Decrypt(eSCO[6]),
                self.encryptorDecryptor.Decrypt(eSCO[7]),
                self.encryptorDecryptor.Decrypt(eSCO[8]),
                self.encryptorDecryptor.Decrypt(eSCO[9]),
                self.encryptorDecryptor.Decrypt(eSCO[10]),
                self.encryptorDecryptor.Decrypt(eSCO[11]),
                self.encryptorDecryptor.Decrypt(eSCO[12]),
                self.encryptorDecryptor.Decrypt(eSCO[13]),
                self.encryptorDecryptor.Decrypt(eSCO[14])
                )
            decryptedscooters.append(tempScooter)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"{self.RepeatString(' ', 25, 'brand')} | {self.RepeatString(' ', 25, 'model')} | {self.RepeatString(' ', 25, 'Serial number')} | {self.RepeatString(' ', 25, 'Top speed')} | {self.RepeatString(' ', 25, 'Battery Capacity')} | {self.RepeatString(' ', 25, 'State of Charge')} | {self.RepeatString(' ', 25, 'Target-range SoC')} | {self.RepeatString(' ', 25, 'Location')} | {self.RepeatString(' ', 25, 'Out-of-service status')} | {self.RepeatString(' ', 25, 'Mileage')} | {self.RepeatString(' ', 25, 'Last maintenance date')} |")
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(decryptedscooters)):
            print(f"""| [{a + 1}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 25, decryptedscooters[a].Brand)} | {self.RepeatString(' ', 25, decryptedscooters[a].Model)} | {self.RepeatString(' ', 25, decryptedscooters[a].SerialNumber)} | {self.RepeatString(' ', 25, decryptedscooters[a].TopSpeed)} | {self.RepeatString(' ', 25, decryptedscooters[a].BatteryCapacity)} | {self.RepeatString(' ', 25, decryptedscooters[a].StateOfCharge)} | {self.RepeatString(' ', 25, f"{decryptedscooters[a].TargetRangeMin}-{decryptedscooters[a].TargetRangeMax}")} | {self.RepeatString(' ', 25, f"{decryptedscooters[a].LocationLat}-{decryptedscooters[a].LocationLong}")}  | {self.RepeatString(' ', 25, decryptedscooters[a].OutOfService)} | {self.RepeatString(' ', 25, decryptedscooters[a].Mileage)} | {self.RepeatString(' ', 25, decryptedscooters[a].LastMaintenanceDate)} |""")
            print("----------------------------------------------------------------------------------------------------------------------")
        choice = input("Choose a scooter: ")
        if (not InputValidator.IsValidChoiceInput(choice, len(decryptedscooters)+1)): return 13
        print("\n\n")

        choice2 = "1"
        if (self.LoggedInEmployee.Role != "ServiceEngineer"):
            print("[1] edit scooter")
            print("[2] remove scooter")
            choice2 = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice2, 2)): return 13
        if (choice2 == "2"):
            self.DB.DeleteScooter(decryptedscooters[int(choice) - 1].ID)
            self.Logger(self.LoggedInEmployee.Username, f"removed scooter {decryptedscooters[int(choice) - 1].ID}", "", "no")
            print("removed scooter. Returning to homescreen")
            return 1
        print("Editing scooter")
        newScooter = Scooter()
        newScooter.ID = decryptedscooters[int(choice) - 1].ID
        if (not self.AddOrEditScooter(newScooter, decryptedscooters[int(choice) - 1])): return 13
        self.DB.UpdateScooter(newScooter, newScooter.ID)
        print("Edited scooter. Returning to home screen...")
        self.Logger(self.LoggedInEmployee.Username, "Edited a scooter", "", "no")
        sleep(1)
        return 1

class AddTravellerScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering add new traveler screen", "", "no")
        print("Fill in the information for a new traveler \n")
        newTraveller = Traveller()
        if (not self.AddOrEditTraveller(newTraveller)): return 14
        self.DB.AddTraveller(newTraveller)
        print("Saved new traveller. Returning to home screen...")
        self.Logger(self.LoggedInEmployee.Username, "added a new traveller", "", "no")
        sleep(1)
        return 1

class EditOrRemoveTraveller(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering edit or delete traveller screen", "", "no")
        encryptedTravellers = self.DB.GetAllTravellers()
        decryptedTravellers = []
        for eTraveller in encryptedTravellers:
            tempTraveller = Traveller(
                eTraveller[0],
                self.encryptorDecryptor.Decrypt(eTraveller[1]),
                self.encryptorDecryptor.Decrypt(eTraveller[2]),
                self.encryptorDecryptor.Decrypt(eTraveller[3]),
                self.encryptorDecryptor.Decrypt(eTraveller[4]),
                self.encryptorDecryptor.Decrypt(eTraveller[5]),
                self.encryptorDecryptor.Decrypt(eTraveller[6]),
                self.encryptorDecryptor.Decrypt(eTraveller[7]),
                self.encryptorDecryptor.Decrypt(eTraveller[8]),
                self.encryptorDecryptor.Decrypt(eTraveller[9]),
                self.encryptorDecryptor.Decrypt(eTraveller[10]),
                self.encryptorDecryptor.Decrypt(eTraveller[11]),
                self.encryptorDecryptor.Decrypt(eTraveller[12])
                )
            decryptedTravellers.append(tempTraveller)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 25, 'Firstname')} | {self.RepeatString(' ', 25, 'Lastname')} | {self.RepeatString(' ', 25, 'Birthday')} | {self.RepeatString(' ', 25, 'Gender')} | {self.RepeatString(' ', 25, 'Streetname')} | {self.RepeatString(' ', 25, 'House number')} | {self.RepeatString(' ', 25, 'Zipcode')} | {self.RepeatString(' ', 25, 'City')} | {self.RepeatString(' ', 25, 'Email')} | {self.RepeatString(' ', 25, 'Phone number')} | {self.RepeatString(' ', 25, 'Drivingslicence')} | {self.RepeatString(' ', 25, 'Registration date')} |")                    
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(decryptedTravellers)):
            print(f"| [{a + 1}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 25, decryptedTravellers[a].Firstname)} | {self.RepeatString(' ', 25, decryptedTravellers[a].Lastname)} | {self.RepeatString(' ', 25, decryptedTravellers[a].Birthday)} | {self.RepeatString(' ', 25, decryptedTravellers[a].Gender)} | {self.RepeatString(' ', 25, decryptedTravellers[a].StreetName)} | {self.RepeatString(' ', 25, decryptedTravellers[a].HouseNumber)} | {self.RepeatString(' ', 25, decryptedTravellers[a].ZipCode)} | {self.RepeatString(' ', 25, decryptedTravellers[a].City)} | {self.RepeatString(' ', 25, decryptedTravellers[a].Email)} | {self.RepeatString(' ', 25, decryptedTravellers[a].PhoneNumber)} | {self.RepeatString(' ', 25, decryptedTravellers[a].DrivingLicenseNumber)} | {self.RepeatString(' ', 25, decryptedTravellers[a].RegistrationDate)} |")
            print("----------------------------------------------------------------------------------------------------------------------")
        choice = input("Choose a Traveller: ")
        if (not InputValidator.IsValidChoiceInput(choice, len(decryptedTravellers))): return 15
        print("\n\n")

        print("[1] edit traveller")
        print("[2] remove traveller")
        choice2 = input("Make a choice: ")
        if (not InputValidator.IsValidChoiceInput(choice2, 2)): return 15
        if (choice2 == "2"):
            self.DB.DeleteTraveller(decryptedTravellers[int(choice) - 1][0])
            print("removed traveller. Returning to homescreen")
            self.Logger(self.LoggedInEmployee.Username, "removed traveller", "", "no")
            sleep(1)
            return 1
        print("Editing traveller")
        #newScooter.ID = decryptedscooters[int(choice) - 1].ID
        #if (not self.AddOrEditScooter(newScooter, decryptedscooters[int(choice) - 1])): return 13
        #self.DB.UpdateScooter(newScooter, newScooter.ID)
        newTraveller = Traveller()
        newTraveller.CustomerID = decryptedTravellers[int(choice) - 1].CustomerID
        print(newTraveller.CustomerID)
        if (not self.AddOrEditTraveller(newTraveller)): return 15
        self.DB.UpdateTraveller(newTraveller, newTraveller.CustomerID)
        print("Edited traveller. Returning to home screen...")
        self.Logger(self.LoggedInEmployee.Username, "edited traveller", "", "no")
        sleep(1)
        return 1
    
class SearchTraveller(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering search traveller screen", "", "no") 
        encryptedTraveller = self.DB.GetAllTravellers()
        decryptedTraveller: list[Traveller] = []
        hits = []
        for eSCO in encryptedTraveller:
            tempTravelller = Traveller(
                eSCO[0],
                self.encryptorDecryptor.Decrypt(eSCO[1]),
                self.encryptorDecryptor.Decrypt(eSCO[2]),
                self.encryptorDecryptor.Decrypt(eSCO[3]),
                self.encryptorDecryptor.Decrypt(eSCO[4]),
                self.encryptorDecryptor.Decrypt(eSCO[5]),
                self.encryptorDecryptor.Decrypt(eSCO[6]),
                self.encryptorDecryptor.Decrypt(eSCO[7]),
                self.encryptorDecryptor.Decrypt(eSCO[8]),
                self.encryptorDecryptor.Decrypt(eSCO[9]),
                self.encryptorDecryptor.Decrypt(eSCO[10]),
                self.encryptorDecryptor.Decrypt(eSCO[11]),
                self.encryptorDecryptor.Decrypt(eSCO[12])
                )
            decryptedTraveller.append(tempTravelller)
    
        
        searchString = input("Search string: ")  #input checking!!!
        if (not InputValidator.IsValidSearchInput(searchString)): return 17
        for dTRA in decryptedTraveller:
            if (searchString in dTRA.Firstname.lower() or searchString in dTRA.Lastname.lower() or searchString in dTRA.Birthday.lower() or searchString in dTRA.Gender.lower() or searchString in dTRA.StreetName.lower()
            or searchString in str(dTRA.HouseNumber) or searchString in dTRA.ZipCode.lower() or searchString in dTRA.City.lower() or searchString in dTRA.Email.lower()
            or searchString in dTRA.PhoneNumber or searchString in dTRA.DrivingLicenseNumber or searchString in dTRA.RegistrationDate.lower()):  
                hits.append(dTRA)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"{self.RepeatString(' ', 25, 'Firstname')} | {self.RepeatString(' ', 25, 'Lastname')} | {self.RepeatString(' ', 25, 'Birthday')} | {self.RepeatString(' ', 25, 'Gender')} | {self.RepeatString(' ', 25, 'StreetName')} | {self.RepeatString(' ', 25, 'HouseNumber')} | {self.RepeatString(' ', 25, 'ZipCode')} | {self.RepeatString(' ', 25, 'City')} | {self.RepeatString(' ', 25, 'Email')} | {self.RepeatString(' ', 25, 'PhoneNumber')} | {self.RepeatString(' ', 25, 'DrivingLicenseNumber')} |")                    
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(hits)):
            print(f"{self.RepeatString(' ', 25, hits[a].Firstname)} | {self.RepeatString(' ', 25, hits[a].Lastname)} | {self.RepeatString(' ', 25, hits[a].Birthday)} | {self.RepeatString(' ', 25, hits[a].Gender)} | {self.RepeatString(' ', 25, hits[a].StreetName)} | {self.RepeatString(' ', 25, hits[a].HouseNumber)} | {self.RepeatString(' ', 25, hits[a].ZipCode)} | {self.RepeatString(' ', 25, hits[a].City)} | {self.RepeatString(' ', 25, hits[a].Email)} | {self.RepeatString(' ', 25, hits[a].PhoneNumber)} | {self.RepeatString(' ', 25, hits[a].DrivingLicenseNumber)} |")
            print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("\n")
        choice = input("Press [1] to return to home screen: ")
        if (not InputValidator.IsValidChoiceInput(choice, 1)): return 1
        return 1
    
class ShowTraveller(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering show traveller screen", "", "no")
        encryptedTraveller = self.DB.GetAllTravellers()
        decryptedTraveller = []
        for eSCO in encryptedTraveller:
            tempTravelller = Traveller(
                eSCO[0],
                self.encryptorDecryptor.Decrypt(eSCO[1]),
                self.encryptorDecryptor.Decrypt(eSCO[2]),
                self.encryptorDecryptor.Decrypt(eSCO[3]),
                self.encryptorDecryptor.Decrypt(eSCO[4]),
                self.encryptorDecryptor.Decrypt(eSCO[5]),
                self.encryptorDecryptor.Decrypt(eSCO[6]),
                self.encryptorDecryptor.Decrypt(eSCO[7]),
                self.encryptorDecryptor.Decrypt(eSCO[8]),
                self.encryptorDecryptor.Decrypt(eSCO[9]),
                self.encryptorDecryptor.Decrypt(eSCO[10]),
                self.encryptorDecryptor.Decrypt(eSCO[11]),
                self.encryptorDecryptor.Decrypt(eSCO[12])
                )
            decryptedTraveller.append(tempTravelller)

        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"{self.RepeatString(' ', 25, 'Firstname')} | {self.RepeatString(' ', 25, 'Lastname')} | {self.RepeatString(' ', 25, 'Birthday')} | {self.RepeatString(' ', 25, 'Gender')} | {self.RepeatString(' ', 25, 'StreetName')} | {self.RepeatString(' ', 25, 'HouseNumber')} | {self.RepeatString(' ', 25, 'ZipCode')} | {self.RepeatString(' ', 25, 'City')} | {self.RepeatString(' ', 25, 'Email')} | {self.RepeatString(' ', 25, 'PhoneNumber')} | {self.RepeatString(' ', 25, 'DrivingLicenseNumber')} |")                    
        print("----------------------------------------------------------------------------------------------------------------------")
        for a in range(len(decryptedTraveller)):
            print(f"{self.RepeatString(' ', 25, decryptedTraveller[a].Firstname)} | {self.RepeatString(' ', 25, decryptedTraveller[a].Lastname)} | {self.RepeatString(' ', 25, decryptedTraveller[a].Birthday)} | {self.RepeatString(' ', 25, decryptedTraveller[a].Gender)} | {self.RepeatString(' ', 25, decryptedTraveller[a].StreetName)} | {self.RepeatString(' ', 25, decryptedTraveller[a].HouseNumber)} | {self.RepeatString(' ', 25, decryptedTraveller[a].ZipCode)} | {self.RepeatString(' ', 25, decryptedTraveller[a].City)} | {self.RepeatString(' ', 25, decryptedTraveller[a].Email)} | {self.RepeatString(' ', 25, decryptedTraveller[a].PhoneNumber)} | {self.RepeatString(' ', 25, decryptedTraveller[a].DrivingLicenseNumber)} |")
            print("----------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("\n")
        choice = input("Press [1] to return to home screen: ")
        if (not InputValidator.IsValidChoiceInput(choice, 1)): return 1
        return 1