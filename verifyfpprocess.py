import psutil
import os
import getfileprops
import time

def verifyrunningonly(path): # Essa função é para verificar se o executável que é especificado no path está rodando nos processos ou não, essa função é pra verificar se o flashplayer está rodando ou não.
    PIDS = psutil.pids()
    for PID in PIDS:
        try:
            if path.lower() in psutil.Process(PID).cmdline()[0].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess, IndexError):
            pass
    return False    
def verifyfpprocess(MODE): # Essa função serve para poder verificar todos os processos dos sistemas, para assim pegar os directórios deles para verificar se os executáveis deles contém nos detalhes no FileDescription "Adoble Flash Player", se tiver, retorna uma LIST com um valor boleano e uma path, o valor boleano é pra falar que está executando. PS: O mode é para definir se quer encontrar a versão de debug ou standard do flash.
    PIDS = psutil.pids()
    PATHS = []
    for PID in PIDS:
        try:
            PATHS.append(psutil.Process(PID).cmdline()[0])
        except (IndexError, psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            pass
        time.sleep(7.5/1000)
    
    for PATH in PATHS:
        try:
            FILESIZE = round(os.path.getsize(PATH)/2**20)
        except FileNotFoundError:
            pass
        props = None
        if MODE == "S":
            try:
                props = getfileprops.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1 and FILESIZE < 16:
                    return [True, PATH]
            except:
                pass
        elif MODE == "D":
            try:
                props = getfileprops.get_file_properties(path)
                if props["StringFileInfo"]["FileDescription"].find("Adobe Flash Player") != -1 and FILESIZE > 15:
                    return [True, PATH]
            except:
                pass
        time.sleep(7.5/1000)
    return [False, False]
