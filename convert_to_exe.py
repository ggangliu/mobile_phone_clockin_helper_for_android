import os

os.system("pyinstaller -F autoClockIn.py")
os.system("copy config.ini dist\config.ini")