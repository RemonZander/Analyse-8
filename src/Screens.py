import secrets
from time import sleep
from screen import Screen
from Types import Employee, Address, Member
from InputValidation import ValidateInput
from datetime import date
import datetime
import re
import bcrypt
import logging
import os
import base64 
import shutil
from zipfile import ZipFile

class LoginScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        print("Login into Uninue Meal member managment system")
        username = ""
        password = ""
        isLoggedIn = False
        tries = 0
        while isLoggedIn == False and tries < 3:
            username = ValidateInput("", "filling in username", "Username: ", str, lambda x : re.match(r"^[a-zA-Z0-9_'.]+$", x)).lower()
            password = input("password: ")          
            if (not re.match(r"^[a-zA-Z0-9~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{1,30}$", password)):
                print("Login Failed, try again...")
                if (tries == 2):
                        self.Logger("", "login", f"username: {username} failed to login", "yes", logging.WARNING)
                else:                                                                
                    self.Logger("", "login", f"username: {username} failed to login", "no", logging.INFO)
                sleep(2)
                tries += 1
                continue
            if (bcrypt.checkpw(password.encode('utf-8'), "$2b$12$1o2X5GFG17t5BRO/5uIQsO37.Fw.TcH5aa1Mr75FoKpjn4P2lUYxy".encode('utf-8')) and username == "super_admin"):
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
            return 11
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print("welcome super administrator\n\n")
            print("################################################################")
            print("# [1] add new system administrator or consultant               #")
            print("# [2] edit or remove a system administrator or consultant      #")
            print("# [3] add new member                                           #")
            print("# [4] edit or remove a member                                  #")
            print("# [5] display list of users with their roles                   #")
            print("# [6] display list of members                                  #")
            print("# [7] reset consultant password                                #")
            print("# [8] reset system admin password                              #")
            print("# [9] manage backups                                           #")
            print("# [10] display log files                                       #")
            print("# [11] search member                                           #")
            print("# [12] exit program                                            #")
            print("################################################################\n")
            choice = ValidateInput(self.LoggedInEmployee.Username, "Choosing home menu item", "Make a choice: ", int, lambda x : x > 0 and x < 13 and re.match(r"^\d+$", str(x)), 2)
            
            if (choice == 1):
                return 2
            elif (choice == 2):
                return 3
            elif (choice == 3):
                return 4
            elif (choice == 4):
                return 5
            elif (choice == 5):
                return 6
            elif (choice == 6):
                return 7
            elif (choice == 7):
                return 8
            elif (choice == 8):
                return 9
            elif (choice == 9):
                return 12                            
            elif (choice == 10):
                return 10
            elif (choice == 11):
                return 13                            
            elif (choice == 12):
                return -1            
        
        elif (self.LoggedInEmployee.Role == "SystemAdmin"):
            print("welcome system administrator\n\n")
            print("##############################################")
            print("# [1] add new consultant                     #")
            print("# [2] edit or remove a consultant            #")
            print("# [3] add new member                         #")
            print("# [4] edit or remove a member                #")
            print("# [5] display list of users with their roles #")
            print("# [6] display list of members                #")
            print("# [7] reset consultant password              #")
            print("# [8] manage backups                         #")
            print("# [9] display log files                      #")
            print("# [10] search member                         #")
            print("# [11] update own password                   #")            
            print("# [12] exit program                          #")
            print("##############################################\n")
            choice = ValidateInput(self.LoggedInEmployee.Username, "Choosing home menu item", "Make a choice: ", int, lambda x : x > 0 and x < 13 and re.match(r"^\d+$", str(x)), 2)
            
            if (choice == 1):
                return 2
            elif (choice == 2):
                return 3
            elif (choice == 3):
                return 4
            elif (choice == 4):
                return 5
            elif (choice == 5):
                return 6
            elif (choice == 6):
                return 7
            elif (choice == 7):
                return 8
            elif (choice == 8):
                return 12            
            elif (choice == 9):
                return 10
            elif (choice == 10):
                return 13                            
            elif (choice == 11):
                return 11                           
            elif (choice == 12):
                return -1
        else:
            print("welcome consultant\n\n")
            print("####################################")
            print("# [1] add new member               #")
            print("# [2] edit a member                #")
            print("# [3] display list of members      #")
            print("# [4] update own password          #")
            print("# [5] search member                #")
            print("# [6] exit program                 #")
            print("####################################\n")
            choice = ValidateInput(self.LoggedInEmployee.Username, "Choosing home menu item", "Make a choice: ", int, lambda x : x > 0 and x < 7 and re.match(r"^\d+$", str(x)), 1)
            if (choice == 1):
                return 4
            elif (choice == 2):
                return 5
            elif (choice == 3):
                return 7
            elif (choice == 4):
                return 11
            elif (choice == 5):
                return 13                          
            elif (choice == 6):
                return -1
        return 1


class AddSysAdminOrConsultantScreen(Screen):
    def __init__(self):
        pass   

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering add sys admin / consultant screen", "", "no")        
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print("Fill in the information for the new system administrator or consultant:\n")
        else:
            print("Fill in the information for the new consultant:\n")
        newSysAdmin = Employee()       
        newSysAdmin.Firstname = ValidateInput(self.LoggedInEmployee.Username, "adding new user firstname", "Firstname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
        newSysAdmin.Lastname = ValidateInput(self.LoggedInEmployee.Username, "adding new user lastname", "Lastname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
        if (self.LoggedInEmployee.Role == "SuperAdmin"):
            print()
            print("Choose Role: ")
            print("[1] system admin")
            print("[2] consultant")
            choice = ValidateInput(self.LoggedInEmployee.Username, "choosing role for new user", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
            if (choice == 1):
                newSysAdmin.Role = "SystemAdmin"
            elif (choice == 2):
                newSysAdmin.Role = "Consultant"
        else:
            newSysAdmin.Role = "Consultant"                            
        newSysAdmin.Username = ValidateInput(self.LoggedInEmployee.Username, "adding new user username", "Username: ", str, lambda x: re.match(r"^(?=.*[a-zA-Z_])[a-zA-Z0-9_'.]{8,10}$", x)).lower()
        newSysAdmin.Password = ValidateInput(self.LoggedInEmployee.Username, "adding new user password", "Password: ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))

        self.DB.AddSysAdmin(newSysAdmin)
        self.Logger(self.LoggedInEmployee.Username, f"saving new {'sys admin' if newSysAdmin.Role == 'SystemAdmin' else 'consultant'} {newSysAdmin.Username}", "", "no")
        print(f"Saved {'system admin' if newSysAdmin.Role == 'SystemAdmin' else 'consultant'}. Returning to main menu...")
        sleep(1)
        return 1

class EditSysAdminOrConsultantScreen(Screen):
    def __init__(self):
        pass
            
    def DoWork(self):       
        self.Logger(self.LoggedInEmployee.Username, "entering edit or delete sys admin / consultant screen", "", "no")        
        employees = []                               
        if (self.LoggedInEmployee.Role == "SuperAdmin"):        
            print("[1] Edit system admin")
            print("[2] Edit consultant")
            choice4 = ValidateInput(self.LoggedInEmployee.Username, "chosing type of user to edit", "Choose option: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
            if (choice4 == 1):
                 employees =  self.DB.GetAllSysAdmins()
            else:
                employees = self.DB.GetAllConsultants()
        else:          
            employees = self.DB.GetAllConsultants()
        print("----------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")                    
        print("----------------------------------------------------------------------------------")        
        for a in range(len(employees)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("----------------------------------------------------------------------------------")
            
        choice = ValidateInput(self.LoggedInEmployee.Username, "Chosing user to edit", f"Choose {'system admin' if choice4 == 1 else 'Consultant'}: ", int, lambda x : x >= 0 and x < len(employees) and re.match(r"^\d+$", str(x)))
        print("\n\n")
        print("[1] edit user")
        print("[2] remove user")
        choice2 = ValidateInput(self.LoggedInEmployee.Username,"chosing action (edit or remove user)", "Choose option: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
        if (choice2 == 1):
            UpdatedEmployee = Employee()
            print(f"Current firstname: {self.encryptorDecryptor.Decrypt(employees[choice][1])}")
            UpdatedEmployee.Firstname = ValidateInput(self.LoggedInEmployee.Username, "editing firstname", "New firstname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
            print(f"Current lastname: {self.encryptorDecryptor.Decrypt(employees[choice][2])}")
            UpdatedEmployee.Lastname = ValidateInput(self.LoggedInEmployee.Username, "editing lastname", "New lastname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
            if (self.LoggedInEmployee.Role == "SuperAdmin"):
                print("Choose Role: ")
                print("[1] system admin")
                print("[2] consultant")
                choice3 = ValidateInput(self.LoggedInEmployee.Username, "chosing role", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
                if (choice3 == 1):
                    UpdatedEmployee.Role = "SystemAdmin"
                elif (choice3 == 2):
                    UpdatedEmployee.Role = "Consultant"
            else:
                 UpdatedEmployee.Role = self.encryptorDecryptor.Decrypt(employees[choice][3])
            print(f"Current username: {self.encryptorDecryptor.Decrypt(employees[choice][4])}")
            UpdatedEmployee.Username = ValidateInput(self.LoggedInEmployee.Username, "editing username", "Username: ", str, lambda x: re.match(r"^(?=.*[a-zA-Z_])[a-zA-Z0-9_'.]{8,10}$", x)).lower()
            self.DB.UpdateEmployee(UpdatedEmployee, int(self.encryptorDecryptor.Decrypt(employees[choice][0])))
            self.Logger(self.LoggedInEmployee.Username, f"edited {'sys admin' if UpdatedEmployee.Role == 'SystemAdmin' else 'consultant'} {UpdatedEmployee.Username}", "", "no")            
            print(f"Updated {'system admin' if choice4 == 1 else 'Consultant'}. Returning to home screen...")
            sleep(1)
        elif (choice2 == 2):
            self.DB.RemoveEmployee(int(self.encryptorDecryptor.Decrypt(employees[choice][0])))
            self.Logger(self.LoggedInEmployee.Username, f"removed {'sys admin' if self.encryptorDecryptor.Decrypt(employees[choice][3]) == 'SystemAdmin' else 'consultant'} {self.encryptorDecryptor.Decrypt(employees[choice][4])}", "", "no")
            print(f"Removed {'system admin' if choice4 == 1 else 'Consultant'}. Returning to home screen...")
            sleep(1)
        return 1

class AddNewMemberScreen(Screen):
    def __init__(self):
        pass
            
    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering add new member screen", "", "no")       
        print("Fill in the information for a new memberL \n")
        newMember = Member()
        memberAddress = Address()
        newMember.Firstname = ValidateInput(self.LoggedInEmployee.Username, "adding firstname to new member", "Firstname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
        newMember.Lastname = ValidateInput(self.LoggedInEmployee.Username, "adding lastname to new member", "Lastname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
        newMember.Age = ValidateInput(self.LoggedInEmployee.Username, "adding age to new member", "Age: ", int, lambda x : x > 0 and x < 200 and re.match(r"^\d+$", str(x)), 3)
        print("[1] male")
        print("[2] female")
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing gender for new member", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
        if (choice == 1):                                
            newMember.Gender = "male"
        else:
            newMember.Gender = "female"
        newMember.Weight = ValidateInput(self.LoggedInEmployee.Username, "adding weight to new member", "Weight (kg): ", float, lambda x : x > 0 and re.match(r"^\d+(\.\d+)?$", str(x)))
        newMember.Email = ValidateInput(self.LoggedInEmployee.Username, "adding email to new member", "Email: ", str, lambda x : re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", x))
        newMember.PhoneNumber = ValidateInput(self.LoggedInEmployee.Username, "adding phone number to new member", "Phone number (06-12345678): ", str, lambda x : re.match(r"^06-\d{8}$", x), 11)
        memberAddress.StreetName = ValidateInput(self.LoggedInEmployee.Username, "adding streetname to new member", "Streetname: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
        memberAddress.HouseNumber = ValidateInput(self.LoggedInEmployee.Username, "adding housenumber to new member", "Housenumner: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
        memberAddress.ZipCode = ValidateInput(self.LoggedInEmployee.Username, "adding zipcode to new member", "Zipcode (1212AB): ", str, lambda x : re.match(r"^\d{4}[A-Za-z]{2}$", x), 6).upper()
        memberAddress.City = ValidateInput(self.LoggedInEmployee.Username, "adding city to new member", "City: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
        newMember.Address = memberAddress
        currentYear = str(date.today().year)[-2:]
        UID = currentYear
        total = int(UID[0])
        total += int(UID[1])
        for a in range(7):
            num = secrets.randbelow(10)
            UID += str(num)
            total += num
        UID += str(total % 10)
        newMember.UID = UID
        self.DB.AddNewMember(newMember)
        self.Logger(self.LoggedInEmployee.Username, f"saved member {newMember.Firstname + ' ' + newMember.Lastname}", "", "no")        
        print("Saved new member. Returning to home screen...")
        sleep(1)
        return 1

class EditOrRemoveMember(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering edit or delete member screen", "", "no")        
        members = self.DB.GetAllMembers()  
        print("----------------------------------------------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'age')} | {self.RepeatString(' ', 15, 'gender')} | {self.RepeatString(' ', 15, 'email')} | {self.RepeatString(' ', 15, 'phone number')} |")                    
        print("----------------------------------------------------------------------------------------------------------------------")        
        for a in range(len(members)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][4]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][5]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][11]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][12]))} |")
            print("----------------------------------------------------------------------------------------------------------------------")
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing member to edit or remove", "Choose member: ", int, lambda x : x >= 0 and x < len(members) and re.match(r"^\d+$", str(x)))
        print("\n\n")
        choice2 = 1
        if (self.LoggedInEmployee.Role != "Consultant"):                
            print("[1] edit memeber")
            print("[2] remove memeber")
            choice2 = ValidateInput(self.LoggedInEmployee.Username, "chosing action on member", "Choose option: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
        if (choice2 == 1):
            updatedMember = Member()
            print(f"Current firtname: {self.encryptorDecryptor.Decrypt(members[choice][2])}")
            updatedMember.Firstname = ValidateInput(self.LoggedInEmployee.Username, "editing firstname of member", "Firstname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
            print(f"Current lastname: {self.encryptorDecryptor.Decrypt(members[choice][3])}")
            updatedMember.Lastname = ValidateInput(self.LoggedInEmployee.Username, "editing lastname of member", "Lastname: ", str, lambda x : re.match(r"^[A-Za-z\s'-]+$", x))
            print(f"Current age: {self.encryptorDecryptor.Decrypt(members[choice][4])}")
            updatedMember.Age = ValidateInput(self.LoggedInEmployee.Username, "editing age of member", "Age: ", int, lambda x : x > 0 and x < 200 and re.match(r"^\d+$", str(x)), 3)
            print(f"Current gender: {self.encryptorDecryptor.Decrypt(members[choice][5])}")
            print("[1] male")
            print("[2] female")
            choice3 = ValidateInput(self.LoggedInEmployee.Username, "chosing new gender for member", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
            if (choice3 == 1):                                
                updatedMember.Gender = "male"
            else:
                updatedMember.Gender = "female"
            print(f"Curent Weight: {self.encryptorDecryptor.Decrypt(members[choice][6])}")
            updatedMember.Weight = ValidateInput(self.LoggedInEmployee.Username, "editing weight of member", "Weight (kg): ", float, lambda x : x > 0 and re.match(r"^\d+(\.\d+)?$", str(x)), 3)
            print(f"Current Email: {self.encryptorDecryptor.Decrypt(members[choice][11])}")
            updatedMember.Email = ValidateInput(self.LoggedInEmployee.Username, "editing email of member", "Email: ", str, lambda x : re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", x))
            print(f"Current phone number: {self.encryptorDecryptor.Decrypt(members[choice][12])}")
            updatedMember.PhoneNumber = ValidateInput(self.LoggedInEmployee.Username, "editing phone number of member", "Phone number (06-12345678): ", str, lambda x : re.match(r"^06-\d{8}$", x), 11)
            print("Update address?")
            print("[1] yes")
            print("[2] no")
            updatedMember.Address = Address()            
            choice4 = ValidateInput(self.LoggedInEmployee.Username, "chosing option to edit address of member", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
            if (choice4 == 1):
                print(f"Current Streetname: {self.encryptorDecryptor.Decrypt(members[choice][7])}")
                updatedMember.Address.StreetName = ValidateInput(self.LoggedInEmployee.Username, "editing streetname of member", "Streetname: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
                print(f"Current house number: {self.encryptorDecryptor.Decrypt(members[choice][8])}")
                updatedMember.Address.HouseNumber = ValidateInput(self.LoggedInEmployee.Username, "editing house number of member", "house number: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
                print(f"Current zipcode: {self.encryptorDecryptor.Decrypt(members[choice][9])}")
                updatedMember.Address.ZipCode = ValidateInput(self.LoggedInEmployee.Username, "editing zipcode of member", "Zipcode (1212AB): ", str, lambda x : re.match(r"^\d{4}[A-Za-z]{2}$"), 6).upper()
                print(f"Current city: {self.encryptorDecryptor.Decrypt(members[choice][10])}")
                updatedMember.Address.City = ValidateInput(self.LoggedInEmployee.Username, "editing city of member", "city: ", str, lambda x : re.match(r"^[A-Za-z0-9\s,.'-\/]+$", x))
            else:              
                updatedMember.Address.StreetName = self.encryptorDecryptor.Decrypt(members[choice][7])
                updatedMember.Address.HouseNumber = self.encryptorDecryptor.Decrypt(members[choice][8])
                updatedMember.Address.ZipCode = self.encryptorDecryptor.Decrypt(members[choice][9])
                updatedMember.Address.City = self.encryptorDecryptor.Decrypt(members[choice][10])
            self.DB.UpdateMember(updatedMember, members[choice][1])
            print("Updated member. Returning to home screen...")
            self.Logger(self.LoggedInEmployee.Username, f"updated member {updatedMember.Firstname + ' ' + updatedMember.Lastname}", "", "no")              
            sleep(1)
            return 1
        else:
            self.DB.RemoveMember(members[choice][1])
            self.Logger(self.LoggedInEmployee.Username, f"removed member {self.encryptorDecryptor.Decrypt(members[choice][2]) + ' ' + self.encryptorDecryptor.Decrypt(members[choice][3])}", "", "no")            
            print("Removed member. Returning to home screen...")
            return 1

class ShowEmployees(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering show employee screen", "", "no")        
        employees =  self.DB.GetAllSysAdmins() +  self.DB.GetAllConsultants()
        print("-------------------------------------------------------")
        print(f"| {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")                    
        print("-------------------------------------------------------")        
        for a in range(len(employees)):
            print(f"| {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("-------------------------------------------------------")
        print("\n")
        print("Press [1] to return to home screen")
        ValidateInput(self.LoggedInEmployee.Username, "exiting employee list", "Choice: ", int, lambda x : x == 1, 1)
        return 1

class ShowMembersScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering show member screen", "", "no")        
        members = self.DB.GetAllMembers()
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"| {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'age')} | {self.RepeatString(' ', 15, 'gender')} | {self.RepeatString(' ', 15, 'email')} | {self.RepeatString(' ', 15, 'phone number')} | {self.RepeatString(' ', 15, 'weight')} | {self.RepeatString(' ', 15, 'Streetname')} | {self.RepeatString(' ', 15, 'House number')} | {self.RepeatString(' ', 15, 'Zipcode')} | {self.RepeatString(' ', 15, 'City')} |")                    
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")        
        for a in range(len(members)):
            print(f"| {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][4]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][5]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][11]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][12]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][6]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][7]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][8]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][9]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(members[a][10]))} |")
            print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("Press [1] to return to home screen")
        ValidateInput(self.LoggedInEmployee.Username, "exiting member list", "Choice: ", int, lambda x : x == 1, 1)
        return 1

class ResetConsultantPassScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "entering reset consultant password screen", "", "no")        
        employees =  self.DB.GetAllConsultants()
        print("----------------------------------------------------------------------------------")
        print(f"| option | {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'role')} | {self.RepeatString(' ', 15, 'username')} |")                    
        print("----------------------------------------------------------------------------------")        
        for a in range(len(employees)):
            print(f"| [{a}]{self.RepeatString(' ', 3, '')} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][1]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][2]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][3]))} | {self.RepeatString(' ', 15, self.encryptorDecryptor.Decrypt(employees[a][4]))} |")
            print("----------------------------------------------------------------------------------")
            
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing consultant", "Choose consultant: ", int, lambda x : x >= 0 and x < len(employees) and re.match(r"^\d+$", str(x)))
        print("\n\n")
        newPassword = ValidateInput(self.LoggedInEmployee.Username, "typing new password for consultant", "Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
        newPassword2 = ValidateInput(self.LoggedInEmployee.Username, "retyping new password for consultant", "Retype password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
        if (newPassword == newPassword2):
            self.DB.UpdatePassword(newPassword, employees[a][0])
            print("Password Updated. Returning to home screen...")
            self.Logger(self.LoggedInEmployee.Username, f"reset password for consultant: {self.encryptorDecryptor.Decrypt(employees[a][4])}", "", "no")            
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
            
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing system admin", "Choose system admin: ", int, lambda x : x >= 0 and x < len(employees) and re.match(r"^\d+$", str(x)))
        print("\n\n")
        newPassword = ValidateInput(self.LoggedInEmployee.Username, "typing new password for system admin", "Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
        newPassword2 = ValidateInput(self.LoggedInEmployee.Username, "retyping new password for system admin", "Retype password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
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
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing logfile", "Choose logfile: ", int, lambda x : x >= 0 and x < len(files) and re.match(r"^\d+$", str(x)))
        print("\n")
        with open(f"./logs/{files[choice]}", "rb") as file:
            for line in file:
                try:
                    print(base64.b64decode(line).rstrip()[:base64.b64decode(line).rstrip().rfind("] ".encode('utf-8')) + 2].decode('utf-8') + self.encryptorDecryptor.Decrypt(base64.b64decode(line).rstrip()[base64.b64decode(line).rstrip().rfind('] '.encode('utf-8')) + 2:]))
                except:
                    pass                
        print("\n")
        print("Press [1] to return to home screen")
        ValidateInput(self.LoggedInEmployee.Username, "exiting log screen", "Choice: ", int, lambda x : x == 1, 1)
        return 1

class UpdatePasswordScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self):
        self.Logger(self.LoggedInEmployee.Username, "Resetting own password", "", "no")
        oldpwd = self.DB.GetPassword(self.LoggedInEmployee.ID)[0][0]   
        if (bcrypt.checkpw(ValidateInput(self.LoggedInEmployee.Username, "validating password", "Type current password: ").encode('utf-8'), oldpwd)):
            newPassword = ValidateInput(self.LoggedInEmployee.Username, "typing new password for system admin", "new Password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
            newPassword2 = ValidateInput(self.LoggedInEmployee.Username, "retyping new password for system admin", "Retype new password (Minimum of 12 characters, at least one lower case letter, on eupper case letter, on digit and one special character): ", str, lambda x: re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$", x))
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
        print("[1] restore a backup")
        print("[2] make a backup")
        choice = ValidateInput(self.LoggedInEmployee.Username, "chosing backup menu option", "Choice: ", int, lambda x : x > 0 and x < 3 and re.match(r"^\d+$", str(x)), 1)
        if (choice == 1):
            files = os. listdir("./backups")
            for a in range(len(files)):
                print(f"[{a}] | Backup: {files[a]}")
            choice = ValidateInput(self.LoggedInEmployee.Username, "chosing backup to restore", "Choose backup: ", int, lambda x : x >= 0 and x < len(files) and re.match(r"^\d+$", str(x)))
            try:
                shutil.rmtree('./logs')
            except :
                pass
            shutil.unpack_archive(f"./backups/{files[choice]}", './')         
            self.Logger(self.LoggedInEmployee.Username, f"Restoring backup: {files[choice]}", "", "no")
            print("Backup has been restored. The program will now shut down...")
            sleep(2)
            return -1                                                
        else:
            filename = f"./backups/backup {datetime.datetime.now().strftime('%H-%M-%S %d-%m-%Y')}"                      
            shutil.make_archive(filename, format='zip', root_dir='.', base_dir='./logs')
            with ZipFile(filename + ".zip",'a') as zip:
                zip.write('./MMSDB.db')
                zip.write('./keys/private_key.pem')                
                zip.write('./keys/public_key.pem') 
            self.Logger(self.LoggedInEmployee.Username, f"Creating backup: {filename}", "", "no")
            print(f"Backup: {filename} has been made. Returning to home screen...")
            sleep(2)
            return 1

class SearchMemeberScreen(Screen):
    def __init__(self):
        pass

    def DoWork(self): 
        encryptedMembers = self.DB.GetAllMembers()
        decryptedMembers = []
        hits = []        
        for eMEM in encryptedMembers:
            tempMember = Member()
            tempMember.UID = eMEM[1]
            tempMember.Firstname = self.encryptorDecryptor.Decrypt(eMEM[2])                                          
            tempMember.Lastname = self.encryptorDecryptor.Decrypt(eMEM[3])                                          
            tempMember.Age = self.encryptorDecryptor.Decrypt(eMEM[4])                                          
            tempMember.Gender = self.encryptorDecryptor.Decrypt(eMEM[5])
            tempMember.Weight = self.encryptorDecryptor.Decrypt(eMEM[6])
            tempMember.Address = Address()                                                      
            tempMember.Address.StreetName = self.encryptorDecryptor.Decrypt(eMEM[7])
            tempMember.Address.HouseNumber = self.encryptorDecryptor.Decrypt(eMEM[8])
            tempMember.Address.ZipCode = self.encryptorDecryptor.Decrypt(eMEM[9])
            tempMember.Address.City = self.encryptorDecryptor.Decrypt(eMEM[10])
            tempMember.Email = self.encryptorDecryptor.Decrypt(eMEM[11])
            tempMember.PhoneNumber = self.encryptorDecryptor.Decrypt(eMEM[12])
            decryptedMembers.append(tempMember) 

        searchString = ValidateInput(self.LoggedInEmployee.Username, "Entering search string", "search text: ", str, lambda x : re.match(r"^[a-zA-Z0-9~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]*$", x)).lower()
        for dMEM in decryptedMembers:
            if (searchString in dMEM.UID or searchString in dMEM.Firstname.lower() or searchString in dMEM.Lastname.lower() or searchString in str(dMEM.Age) or searchString in dMEM.Gender.lower()
            or searchString in str(dMEM.Weight) or searchString in dMEM.Address.StreetName.lower() or searchString in dMEM.Address.HouseNumber.lower() or searchString in dMEM.Address.ZipCode.lower()
            or searchString in dMEM.Address.City.lower() or searchString in dMEM.Email.lower() or searchString in dMEM.PhoneNumber):  
                hits.append(dMEM)
        print("\n")                
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"| {self.RepeatString(' ', 15, 'firstname')} | {self.RepeatString(' ', 15, 'lastname')} | {self.RepeatString(' ', 15, 'age')} | {self.RepeatString(' ', 15, 'gender')} | {self.RepeatString(' ', 15, 'email')} | {self.RepeatString(' ', 15, 'phone number')} | {self.RepeatString(' ', 15, 'weight')} | {self.RepeatString(' ', 15, 'Streetname')} | {self.RepeatString(' ', 15, 'House number')} | {self.RepeatString(' ', 15, 'Zipcode')} | {self.RepeatString(' ', 15, 'City')} |")                    
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")        
        for a in range(len(hits)):
            print(f"| {self.RepeatString(' ', 15, hits[a].Firstname)} | {self.RepeatString(' ', 15, hits[a].Lastname)} | {self.RepeatString(' ', 15, hits[a].Age)} | {self.RepeatString(' ', 15, hits[a].Gender)} | {self.RepeatString(' ', 15, hits[a].Email)} | {self.RepeatString(' ', 15, hits[a].PhoneNumber)} | {self.RepeatString(' ', 15, hits[a].Weight)} | {self.RepeatString(' ', 15, hits[a].Address.StreetName)} | {self.RepeatString(' ', 15, hits[a].Address.HouseNumber)} | {self.RepeatString(' ', 15, hits[a].Address.ZipCode)} | {self.RepeatString(' ', 15, hits[a].Address.City)} |")
            print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("\n")
        print("Press [1] to return to home screen")
        ValidateInput(self.LoggedInEmployee.Username, "exiting member search", "Choice: ", int, lambda x : x == 1, 1)
        return 1                                                                                                           