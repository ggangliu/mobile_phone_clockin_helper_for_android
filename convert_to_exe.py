import os

os.system("pyinstaller -F autoClockIn_wfh.py")
os.system("copy config.ini dist\config.ini")
os.system("mkdir dist\\Tools\\platform-tools")
os.system("copy Tools\\platform-tools\\adb.exe dist\\Tools\\platform-tools")
os.system("copy Tools\\platform-tools\\AdbWinApi.dll dist\\Tools\\platform-tools")
os.system("copy Tools\\platform-tools\\AdbWinUsbApi.dll dist\\Tools\\platform-tools")
os.system("copy Tools\\platform-tools\\fastboot.exe dist\\Tools\\platform-tools")
os.system("copy Tools\\app-uiautomator.apk dist\\")
os.system("copy Tools\\app-uiautomator-test.apk dist\\")
os.system("mkdir dist\\clockin_record")