import threading
import time

import PySimpleGUI as sg


def my_thread():
    while True:
        sg.PopupAnimated(r"D:\OneDrive\Documents\[PYTHON_PROJECTS]\corelibs\corelibs\gui\processing_08.gif", background_color="white")
        time.sleep(.05)


threading.Thread(target=my_thread, daemon=True).start()

while True:
    time.sleep(.05)
