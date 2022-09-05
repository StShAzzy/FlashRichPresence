import sys
if sys.platform != "win32":
    print("This program is only for Windows")
    sys.exit(1)
import psutil
from pypresence import Presence
import time
import win32api
import getfileprops
import verifyfpprocess

if __name__ == "__main__":
    #fp means flashplayer, fpd means flashplayerdebug
    print("Started.")
    rpcrun = False # This is for verifying if the rich presence is running or not.
    already_verified_fps = [False, False] # This is for verifying if verifyfpprocess was already ran or not for flashplayer debug or flashplayer standard.
    fpdinfo = None # The variable for information from flashplayer debug, such as if it's running(true or false) or the flash player debug path.
    fpinfo = None # # The same as the variable above, but for flash player standard.
    type = "Unknown" # The type of flash player, standard or debug mode.
    version = "Unknown" # The variable to save the flash player version.
  
    CLIENT_ID = '1013717821122936873' # Don't change that, please.
    RPC = Presence(client_id) # Client ID connect

    while True:
        time.sleep(1)
        
        if already_verified_fps[0] == False: # This verify if verifyfpprocess already ran to get the flashplayer(standard) info, if it has been already ran, so it won't run again. 
            fpinfo = verifyfpprocess.verifyfpprocess("S") 
        if alreadyverifyfps[1] == False:
            fpdinfo = verifyfpprocess.verifyfpprocess("D")

        if RPCRun:
            fpdinfo[0] = verifyfpprocess.verifyrunningonly(str(fpdinfo[1]))
            fpinfo[0] = verifyfpprocess.verifyrunningonly(str(fpinfo[1]))
        filepropsfp = None
        filepropsfpd = None
        fileversionfpd = None
        fileversionfp = None
        if fpd[0]:
            filepropsfpd = getfileprops.get_file_properties(fpdinfo[1])
            fileversionfpd = filepropsfpd["FileVersion"]
        if fp[0]:
            filepropsfp = getfileprops.get_file_properties(fpinfo[1])
            fileversionfp = filepropsfp["FileVersion"]
        if (fpdinfo[0] or fpinfo[0]) == False:
            print("Didn't found any Flash Player running") 
            if rpcrun:
                RPC.close()
                rpcrun = False
                already_verified_fps[0] = False
                already_verified_fps[1] = False
            continue
        if rpcrun == False:
            RPC.connect()
            rpcrun = True
            if fpinfo[0]:
                already_verified_fps[0] = True
            elif fpdinfo[0]:
                already_verified_fps[1] = True
        if fpdinfo[0] and fpinfo[0]:
            print("Found Debug and Standard Build")      
            version = f"Multiple Running" 
            type = "Multiple Running" 
        elif fpdinfo[0]:
            print("Found Debug Build")
            version = propsfpd['FileVersion']
            type = "Debug"
        elif fpinfo[0]:
            print("Found Standard Build")
            version = propsfp['FileVersion']
            type = "Standard"
        if rpcrun == True:
           RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {version} ({type})")
