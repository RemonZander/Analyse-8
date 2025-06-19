import datetime
from enum import Enum
import base64
class LogLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRYTICAL = 4

class Logger(object):
    def __init__(self, filePath: str, fileMode: str):
        self.filePath = filePath
        self.fileMode = fileMode

    def Log(self, msg, logLevel = LogLevel.INFO):
        file1 = open(self.filePath + datetime.datetime.now().strftime('%H %d-%m-%Y') + ".log", self.fileMode)
        file1.write(base64.b64encode(f"[{datetime.datetime.now().strftime('%H-%M-%S %d-%m-%Y')} {str(logLevel)}] ".encode('utf-8') + msg) + b'\r\n')
        file1.close()