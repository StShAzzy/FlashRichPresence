import psutil
import os
import getfileprops as gp
import time

def verifyrunningonly(dir):
    pids = psutil.pids()
    user = psutil.users()[0][0]
    for proc in psutil.process_iter(['pid', 'username']):
        try:
            if str(proc.info["username"]).find(user) != -1 and dir in psutil.Process(proc.info["pid"]).cmdline()[0]:
                return True
        except (IndexError, psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            pass
    return False

def verifyifdebug(path): # Verifica se o path dado no parâmetro é um Flash Player Debug.
    with open(path, 'rb') as f:
        hexdata = f.read().hex()
        if hexdata.find("006465627567456e74657200") == -1:
            f.close()
            return False
        f.close()
        return True


def verifyfpprocess(mode):
    pids = psutil.pids()
    paths = []
    user = psutil.users()[0][0]
    for proc in psutil.process_iter(['pid', 'username']):
        try:
            if str(proc.info["username"]).find(user) != -1:
                paths.append(psutil.Process(proc.info["pid"]).cmdline()[0])
        except (IndexError, psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            pass

    for path in paths:
        props = 0
        if mode == "S":
            try:
                props = gp.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1:
                    try:
                        debugon = verifyifdebug(path)
                    except FileNotFoundError:
                        continue
                    if debugon == False:
                        return [True, path]
            except:
                pass
        elif mode == "D":
            try:
                props = gp.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1:
                    try:
                        debugon = verifyifdebug(path)
                    except FileNotFoundError:
                        continue
                    if debugon == True:
                        return [True, path]
            except:
                pass
    return [False, False]
