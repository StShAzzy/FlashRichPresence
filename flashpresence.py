import psutil
from pypresence import Presence
import time
import win32api

def checkprocess(targetname):
    for proc in psutil.process_iter():
        try:
            if targetname.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False

def get_file_properties(fname):
    prop_names = ('Comments', 'InternalName', 'ProductName',
                  'CompanyName', 'LegalCopyright', 'ProductVersion',
                  'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                  'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None, 'FileDescription': None}

    fixed_info = win32api.GetFileVersionInfo(fname, '\\')
    props['FixedFileInfo'] = fixed_info
    props['FileVersion'] = "%d.%d.%d.%d" % (fixed_info['FileVersionMS'] / 65536,
                                                fixed_info['FileVersionMS'] % 65536,
                                                fixed_info['FileVersionLS'] / 65536,
                                                fixed_info['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
    lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

    str_info = {}
    for propName in prop_names:
        str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
        str_info[propName] = win32api.GetFileVersionInfo(fname, str_info_path)

    props['StringFileInfo'] = str_info
   # except:
   #     pass

    return props

if __name__ == "__main__":

    print("Started.")
    RPCRun = False
    TYPE = "Unknown"
    VERSION = "Unknown"
  
    client_id = '1013717821122936873'  # Fake ID, put your real one here
    RPC = Presence(client_id)
    fpd = "flashplayer_debug.exe"
    fp = "flashplayer.exe"
    propsfp = get_file_properties(fp)
    propsfpd = get_file_properties(fpd)
    fileversionfp = propsfp["FileVersion"]
    fileversionfpd = propsfpd["FileVersion"]
          
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
        debugon = checkprocess(fpd)
        standardon = checkprocess(fp)            
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
