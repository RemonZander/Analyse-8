import os
from time import sleep

from Screens import (AddScooterScreen, AddSysAdminOrServiceEngineerScreen,
                     AddTravellerScreen, EditOrRemoveScooter,
                     EditOrRemoveTraveller,
                     EditSysAdminOrServiceEngineerScreen, HomeScreen,
                     LoginScreen, ManageBackups, ReadLogsScreen,
                     ResetServiceEngineerScreen, ResetSysAdminPassScreen,
                     SearchScooterScreen, SearchTraveller, ShowEmployees,
                     ShowScootersScreen, ShowTraveller, UpdatePasswordScreen)


def Main():
    #DB.SetupDatabase()
    screens = [
        LoginScreen(),                          #0
        HomeScreen(),                           #1
        AddSysAdminOrServiceEngineerScreen(),   #2
        EditSysAdminOrServiceEngineerScreen(),  #3
        ShowEmployees(),                        #4
        ShowScootersScreen(),                   #5
        ResetServiceEngineerScreen(),           #6
        ResetSysAdminPassScreen(),              #7
        ReadLogsScreen(),                       #8
        UpdatePasswordScreen(),                 #9
        ManageBackups(),                        #10
        SearchScooterScreen(),                  #11
        AddScooterScreen(),                     #12
        EditOrRemoveScooter(),                  #13
        AddTravellerScreen(),                   #14
        EditOrRemoveTraveller(),                #15
        SearchTraveller(),                      #16
        ShowTraveller()                         #17

        ]
    currentScreen = 0
    #os.chdir("C:/")    
    #cmd = 'mode 210,30'
    #os.system(cmd)
                
    while currentScreen != -1 and currentScreen != None:
        os.system('cls')
        currentScreen = screens[currentScreen].DoWork()
        
Main()