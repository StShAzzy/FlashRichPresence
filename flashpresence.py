import psutil
from pypresence import Presence
import time


def checkprocess(targetname):
    for proc in psutil.process_iter():
        try:
            if targetname.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False

if __name__ == "__main__":

    print("Started.")
    DebugRunning = False
    StandaloneRunning = False
    RPCRun = False
    TYPE = "Unknown"
    VERSION = "Unknown"
  
    client_id = '1013717821122936873'  # Fake ID, put your real one here
    RPC = Presence(client_id)
    fpd = "flashplayer_32_sa_debug.exe"
    fp = "flashplayer.exe"
    while True:  # The presence will stay on as long as the program is running
        time.sleep(4)
        
        if checkprocess(fpd) == True:
            print("Found Debug Build")
            TYPE = "Debug"
            if DebugRunning == False and RPCRun == False:
              RPC.connect()
              RPCRun = True
            # RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")
            DebugRunning = True
        else:
            print("Debug Build Not Found")
            if DebugRunning == True and RPCRun == True:
                DebugRunning = False
            if StandaloneRunning == False and RPCRun == True:
                RPCRun = False
                RPC.close()
  
        if checkprocess(fp) == True:
            print("Found Standalone Build")
            TYPE = "Standard"
            if StandaloneRunning == False and RPCRun == False:
              RPC.connect()
              RPCRun = True
             # RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")
            StandaloneRunning = True 
        else:
            print("Standalone Build Not Found")
            if StandaloneRunning == True and RPCRun == True:
                StandaloneRunning = False
            if DebugRunning == False and RPCRun == True:
                RPCRun = False
                RPC.close()
            
        if DebugRunning == True and StandaloneRunning == True:
           TYPE = "Multiple Running"   
        if RPCRun == True:
           RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")