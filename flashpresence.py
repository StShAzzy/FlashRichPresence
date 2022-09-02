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
    """
    Read all properties of the given file return them as a dictionary.
    """
    prop_names = ('Comments', 'InternalName', 'ProductName',
                  'CompanyName', 'LegalCopyright', 'ProductVersion',
                  'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                  'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

   # try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
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
    DebugRunning = False
    StandaloneRunning = False
    RPCRun = False
    TYPE = "Unknown"
    VERSION = "Unknown"
  
    client_id = '1013717821122936873'  # Fake ID, put your real one here
    RPC = Presence(client_id)
    fpd = "flashplayer_debug.exe"
    fp = "flashplayer.exe"
    while True:  # The presence will stay on as long as the program is running
        time.sleep(4)
        
        if checkprocess(fpd) == True:
            print("Found Debug Build")
            TYPE = "Debug"
            props = get_file_properties(fpd)
            #VERSION = props['StringFileInfo']['ProductVersion']
            VERSION = props['FileVersion']
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
            props = get_file_properties(fp)
            #VERSION = props['StringFileInfo']['ProductVersion']
            VERSION = props['FileVersion']
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
           VERSION = "Multiple Running" 
        if RPCRun == True:
           RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {VERSION} ({TYPE})")