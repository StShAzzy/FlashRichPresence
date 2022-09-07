import sys
if sys.platform != "win32":
    print("This program is only for Windows")
    sys.exit(1)
import psutil
import pypresence
import time
import win32api
import getfileprops
import verifyfpprocess
import updaterichpresence

if __name__ == "__main__":
    #fp means flashplayer, fpd means flashplayerdebug
    print("Started.")
    rpcrun = False # This is for verifying if the rich presence is running or not.
    already_verified_fps = [False, False] # This is for verifying if verifyfpprocess was already ran or not for flashplayer debug or flashplayer standard.
    fpdinfo = None # The variable for information from flashplayer debug, such as if it's running(true or false) or the flash player debug path.
    fpinfo = None # # The same as the variable above, but for flash player standard.
    last_verifyfps = [None, None]
    type = "Unknown" # The type of flash player, standard or debug mode.
    version = "Unknown" # The variable to save the flash player version.
    first_runfp = False
    first_runfpd = False
    CLIENT_ID = '1013717821122936873' # Don't change that, please.
    try:
        RPC = pypresence.Presence(CLIENT_ID) # Client ID connect
    except pypresence.exceptions.DiscordNotFound:
        print("Your Discord is not running or not installed!")
        sys.exit(1)
    while True:
        time.sleep(1)
        try:
            last_verifyfps[0] = fpinfo[0]
        except TypeError:
            last_verifyfps[0] = None
        try:
            last_verifyfps[1] = fpdinfo[0]
        except TypeError:
            last_verifyfps[1] = None
        if already_verified_fps[0] == False: # This verify if verifyfpprocess already ran to get the flashplayer(standard) info, if it has been already ran, so it won't run again. 
            fpinfo = verifyfpprocess.verifyfpprocess("S")
        if already_verified_fps[1] == False:
            fpdinfo = verifyfpprocess.verifyfpprocess("D")

        if rpcrun:
            fpdinfo[0] = verifyfpprocess.verifyrunningonly(str(fpdinfo[1]))
            fpinfo[0] = verifyfpprocess.verifyrunningonly(str(fpinfo[1]))
        filepropsfp = None
        filepropsfpd = None
        fileversionfpd = None
        fileversionfp = None
        if fpdinfo[0]:
            filepropsfpd = getfileprops.get_file_properties(fpdinfo[1])
            fileversionfpd = filepropsfpd["FileVersion"]
        if fpinfo[0]:
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
                first_runfp = True
            if fpdinfo[0]:
                already_verified_fps[1] = True
                first_runfpd = True

        if (last_verifyfps[0] == False and last_verifyfps[1] == True) and (fpinfo[0] and fpdinfo[0]):
            first_runfp = True
            first_runfpd = True
        elif last_verifyfps[0] == True and fpinfo[0] == False:
            first_runfpd = True
        if (last_verifyfps[1] == False and last_verifyfps[0] == True) and (fpdinfo[0] and fpinfo[0]):
            first_runfpd = True
            first_runfp = True
        elif last_verifyfps[1] == True and fpdinfo[0] == False:
            first_runfp = True
        if (fpdinfo[0] and fpinfo[0]) and (first_runfp and first_runfpd):
            print("Found Debug and Standard Build")      
            version = "Multiple Running" 
            type = "Multiple Running"
            updaterichpresence.updatepresence(RPC, version, type)
            first_runfp = False
            first_runfpd = False
        elif fpdinfo[0] and first_runfpd:
            print("Found Debug Build")
            version = filepropsfpd['FileVersion']
            type = "Debug"
            updaterichpresence.updatepresence(RPC, version, type)
            first_runfpd = False
        elif fpinfo[0] and first_runfp:
            print("Found Standard Build")
            version = filepropsfp['FileVersion']
            type = "Standard"
            updaterichpresence.updatepresence(RPC, version, type)
            first_runfp = False
