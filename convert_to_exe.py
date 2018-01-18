import os

os.system("pyinstaller -F autoClockIn.py")
os.system("copy config.ini dist\config.ini")
os.system("copy Tools\\adb\\adb.exe dist\\")
os.system("copy Tools\\adb\\AdbWinApi.dll dist\\")
os.system("copy Tools\\adb\\AdbWinUsbApi.dll dist\\")
os.system("copy Tools\\adb\\fastboot.exe dist\\")
os.system("mkdir dist\clockin_record")