import psutil
import os
import getfileprops as gp
import time

def verifyrunningonly(dir):
    pids = psutil.pids()
    for pid in pids:
        try:
            if dir in psutil.Process(pid).cmdline()[0]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess, IndexError):
            pass
    return False    
def verifyfpprocess(mode):
    try:
        mode.lower()
    except:
        pass

    pids = psutil.pids()
    paths = []
    for pid in pids:
        try:
            paths.append(psutil.Process(pid).cmdline()[0])
        except (IndexError, psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            pass
        time.sleep(7.5/1000)
    
    for path in paths:
        try:
            filesize = round(os.path.getsize(path)/2**20)
        except FileNotFoundError:
            pass
        props = 0
        if mode == "S":
            try:
                props = gp.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1 and filesize < 16:
                    return [True, path]
            except:
                pass
        elif mode == "D":
            try:
                props = gp.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1 and filesize > 15:
                    return [True, path]
            except:
                pass
        time.sleep(7.5/1000)
    return [False, False]
