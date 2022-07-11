from ast import While
from asyncio.windows_events import NULL
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
import base64
from tkinter import *
from tkinter import ttk
# import tkMessageBox
import tkinter
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfile
import tkinter.font as font
from datetime import datetime

import os

def logAdd(windoName):
    try:
        if windoName:
            with open("logger.txt", "a+") as file_object:
                now = datetime.now()
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0 :
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write( now.strftime("%d/%m/%Y %H:%M:%S") + ";" +windoName)
    except:
        print('Fail to write')

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None


def startMon():
    loop = True
    windowActive = ""
    while loop:
        if getForegroundWindowTitle() and windowActive != getForegroundWindowTitle():
            logAdd(getForegroundWindowTitle())
            windowActive = getForegroundWindowTitle()
            print(windowActive)

startMon()
