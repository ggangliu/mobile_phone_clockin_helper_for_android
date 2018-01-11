import os

os.system("pyinstaller -F autoClockIn_zsh.py")
os.system("copy config.ini dist\config.ini")