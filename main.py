import sys
assert ("win32" in sys.platform), "This program is only for Windows."
import psutil
from pypresence import Presence
import time
import win32api
import getfileprops as gf
import verifyfpprocess as vp

if __name__ == "__main__":

    print("Started.")
    RPCRun = False
    alreadyverifyfps = [False, False]
    fpd = None
    fp = None
    TYPE = "Unknown"
    VERSION = "Unknown"
  
    client_id = '1013717821122936873'
    RPC = Presence(client_id)

    while True:  # The presence will stay on as long as the program is running
        time.sleep(1)
        if alreadyverifyfps[0] == False: 
            fp = vp.verifyfpprocess("S")
        if alreadyverifyfps[1] == False:
            fpd = vp.verifyfpprocess("D")

        if RPCRun:
            fpd[0] = vp.verifyrunningonly(str(fpd[1]))
            fp[0] = vp.verifyrunningonly(str(fp[1]))
        propsfp = None
        propsfpd = None
        fileversionfpd = None
        fileversionfp = None
        if fpd[0]:
            propsfpd = gf.get_file_properties(fpd[1])
            fileversionfpd = propsfpd["FileVersion"]
        if fp[0]:
            propsfp = gf.get_file_properties(fp[1])
            fileversionfp = propsfp["FileVersion"]
        if (fpd[0] or fp[0]) == False:
            print("Didn't found any Flash Player running") 
            if RPCRun:
                RPC.close()
                RPCRun = False
                alreadyverifyfps[0] = False
                alreadyverifyfps[1] = False
            continue
        if RPCRun == False:
            RPC.connect()
            RPCRun = True
            if fp[0]:
                alreadyverifyfps[0] = True
            elif fpd[0]:
                alreadyverifyfps[1] = True
        if fpd[0] and fp[0]:
            print("Found Debug and Standard Build")
            TYPE = "Multiple Running"       
            VERSION = f"Multiple Running" 
        elif fpd[0]:
            print("Found Debug Build")
            VERSION = propsfpd['FileVersion']
            TYPE = "Debug"
        elif fp[0]:
            print("Found Standard Build")
            VERSION = propsfp['FileVersion']
            TYPE = "Standard"
        if RPCRun == True:
           RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")
