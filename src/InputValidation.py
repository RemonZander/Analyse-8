from Logger import LogLevel
from Logger import Logger
from EncryptionDecryption import EncryptorDecryptor
def ValidateInput(currentUsername: str, currentActivity: str, inputText: str, validationType = str, validationFunction = lambda x : x, maxSize = 50, tries = 0):
    logger = Logger("./logs/", "ab") 
    inputData = ""
    encryptorDecryptor = EncryptorDecryptor()    
    try:
        inputData = input(inputText)
        if (inputData != None and inputData != "" and not ('\0' in inputData) and len(inputData) <= maxSize and validationFunction(validationType(inputData))):
            return validationType(inputData)
        elif (inputData == None or inputData == "" or '\0' in inputData):
            print("An Empty input is not allowed")
            if ('\0' in inputData):
                logger.Log(encryptorDecryptor.Encrypt(f"{currentUsername} - {currentActivity} - filled in null byte. Tries: {tries} - yes"), LogLevel.WARNING)                
            else:
                logger.Log(encryptorDecryptor.Encrypt(f"{currentUsername} - {currentActivity} - filled in empty prompt. Tries: {tries} - {'yes' if tries > 2 else 'no'}"), LogLevel.INFO)                
            return ValidateInput(currentUsername, currentActivity, inputText, validationType, validationFunction, maxSize, tries + 1)                  
        elif (len(inputData) > maxSize):
            print("Your input has too many characters")            
            logger.Log(encryptorDecryptor.Encrypt(f"{currentUsername} - {currentActivity} - filled in prompt is too big. Tries: {tries} - {'yes' if tries > 2 else 'no'}"), LogLevel.INFO)            
            return ValidateInput(currentUsername, currentActivity, inputText, validationType, validationFunction, maxSize, tries + 1)
        else:
            print("Your input is invalid")
            logger.Log(encryptorDecryptor.Encrypt(f"{currentUsername} - {currentActivity} - prompt did not have a correct format. Tries: {tries} - {'yes' if tries > 2 else 'no'}"), LogLevel.INFO)                    
            return ValidateInput(currentUsername, currentActivity, inputText, validationType, validationFunction, maxSize, tries + 1)
    except Exception as e:
        print("An error occured with your input")        
        logger.Log(encryptorDecryptor.Encrypt(f"{currentUsername} - {currentActivity} - there was an error with the prompt. Exception: {e}\n Tries: {tries} - {'yes' if tries > 2 else 'no'}"), LogLevel.WARNING)        
        return ValidateInput(currentUsername, currentActivity, inputText, validationType, validationFunction, maxSize, tries + 1)