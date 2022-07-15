from ast import Not, While
from asyncio.windows_events import NULL
from tokenize import Name
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
import pyautogui
import keyboard 
import time
import sys
import os

input("Durante o monitoramento, pressione <CTRL + K> para pausar ou <CTRL + C> caso deseje encerrar. Pressione <ENTER> agora para iniciar o monitoramento...")

def pauseScript():
    programPause = input("Pressione <ENTER> para continuar...")
    if keyboard.is_pressed('S'):
        logAdd(getForegroundWindowTitle())

    # keyboard.wait('enter')
    # iLoop = True
    # while iLoop:
    #     # time.sleep(1)
        # if keyboard.is_pressed('ctrl + i'):  # if key 'q' is pressed 
        #     print('Monitoramento reiniciado!')
        #     iLoop = False
        # else:
        #     iLoop = True
        # keyboard.wait('esc')
  
nameFile = datetime.now().date()
lasttime = datetime.now()
lastWindow = ""
def logAdd(windowName):
    global lasttime
    global lastWindow
    
    try:
        if lastWindow and lastWindow != "":
            if windowName:
                with open("logger_"+str(nameFile)+".csv", "a+", encoding="utf-8") as file_object:
                    now = datetime.now()
                    diff = now - lasttime
                    # Move read cursor to the start of file.
                    file_object.seek(0)
                    # If file is not empty then append '\n'
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")                        
                    
                    file_object.write( now.strftime("%d/%m/%Y %H:%M:%S") + ";" + lastWindow.replace("\\u25cf", "") + ";" + str(diff))
                    print('write log: ' + lastWindow)
                    lasttime = datetime.now()
                    lastWindow = windowName 
        else:
            lastWindow = windowName
    except NameError:
        print('Fail to write' + str(NameError))

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
    lastmousepos = pyautogui.position()
    lasttime = datetime.now()
    tempo_inativo = 0;
    while loop:
        if keyboard.is_pressed('ctrl + k'):
            pauseScript()
        
        # keyboard.add_hotkey('ctrl + k', ) 
        if getForegroundWindowTitle() and windowActive != getForegroundWindowTitle():
            logAdd(getForegroundWindowTitle())
            windowActive = getForegroundWindowTitle()
            print(windowActive)
            lastmousepos = pyautogui.position()
            lasttimemouse = datetime.now()
        else: 
            #nao trocou de tela, espera 1 segundo
            time.sleep(1)
            mousepos = pyautogui.position()

            #se a posicao do mouse mudou, ta ativo
            if(mousepos != lastmousepos):
                lastmousepos = mousepos
                lasttimemouse = datetime.now()
                print('ativo');
                if(tempo_inativo >= 120):
                    tempo_inativo = 0
                    logAdd('possivel ausencia temporaria > 2min')
            else:
                #tela parada e mouse nao mudou, pode estar inativo
                nowmouse = datetime.now()
                tdelta = nowmouse - lasttimemouse
                tempo_inativo = tdelta.total_seconds()
                print('segundos parado:', tdelta.total_seconds())
                # if(nowmouse)

try:
    startMon()
except KeyboardInterrupt:
    print('Finalizado')
    try:
        logAdd(getForegroundWindowTitle())
        sys.exit(0)
    except SystemExit:
        os._exit(0)

