from Screens import LoginScreen, HomeScreen, AddSysAdminOrConsultantScreen, EditSysAdminOrConsultantScreen, AddNewMemberScreen, EditOrRemoveMember, ShowEmployees, ShowMembersScreen, ResetConsultantPassScreen, ResetSysAdminPassScreen, ReadLogsScreen, UpdatePasswordScreen, ManageBackups, SearchMemeberScreen
import os
def Main():             
    #DB.SetupDatabase()
    screens = [
        LoginScreen(),                          #0
        HomeScreen(),                           #1
        AddSysAdminOrConsultantScreen(),        #2
        EditSysAdminOrConsultantScreen(),       #3
        AddNewMemberScreen(),                   #4
        EditOrRemoveMember(),                   #5
        ShowEmployees(),                        #6
        ShowMembersScreen(),                    #7
        ResetConsultantPassScreen(),            #8
        ResetSysAdminPassScreen(),              #9
        ReadLogsScreen(),                       #10
        UpdatePasswordScreen(),                 #11
        ManageBackups(),                        #12
        SearchMemeberScreen()                   #13

        ]
    currentScreen = 0
    #os.chdir("C:/")    
    #cmd = 'mode 210,30'
    #os.system(cmd)
                
    while currentScreen != -1 and currentScreen != None:
        os.system('cls')
        currentScreen = screens[currentScreen].DoWork()             
        
Main()