import win32api as wapi
import time

keyList = ["\b"]
for char in "UP LEFT RIGHT DOWN":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
