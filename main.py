import psutil
from pypresence import Presence
import time
import win32api
import sys
import checkprocess as cp
import getfileprops as gf

assert ("win32" in sys.platform), "This program is only for Windows."

if __name__ == "__main__":

    print("Started.")
    Mode = "S"
    RPCRun = False
    TYPE = "Unknown"
    VERSION = "Unknown"
  
    client_id = '1013717821122936873'
    RPC = Presence(client_id)
    fpd = "flashplayer_debug.exe"
    fp = "flashplayer.exe"
    try:
        propsfp = gf.get_file_properties(fp)
        propsfpd = gf.get_file_properties(fpd)
        fileversionfp = propsfp["FileVersion"]
        fileversionfpd = propsfpd["FileVersion"]
    except:
        print("There's no Flash Player on the folder that I am!")
        time.sleep(5)
        exit()

    while True:  # The presence will stay on as long as the program is running
        time.sleep(4)
        isfp = propsfp["StringFileInfo"]["FileDescription"].find("Adobe Flash Player")
        isfpd = propsfpd["StringFileInfo"]["FileDescription"].find("Adobe Flash Player")
        if isfp == -1:
            print("Your flashplayer.exe is not a Flash Player")
        elif isfpd == -1:
            print("Your flashplayer_debug.exe is not a Flash Player")
        elif isfp and isfpd == -1:
            print("Both flashplayer.exe and flashplayer.exe are not Flash Player")
            continue
        debugon = cp.checkprocess(fpd)
        standardon = cp.checkprocess(fp)            
        if (debugon or standardon) == False:
            if RPCRun:
                RPC.close()
                RPCRun = False
            continue
        if RPCRun == False:
            RPC.connect()
            RPCRun = True
        if debugon and standardon:
            print("Found Debug and Standard Build")
            TYPE = "Multiple Running"       
            VERSION = f"Multiple Running" 
        elif debugon:
            print("Found Debug Build")
            VERSION = propsfpd['FileVersion']
            TYPE = "Debug"
        elif standardon:
            print("Found Standard Build")
            VERSION = propsfp['FileVersion']
            TYPE = "Standard"
        if RPCRun == True:
           RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")
