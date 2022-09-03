import psutil

def checkprocess(targetname):
    for proc in psutil.process_iter():
        try:
            if targetname.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False