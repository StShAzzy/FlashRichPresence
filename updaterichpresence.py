import pypresence
import time
def updatepresence(RPC, version, type):
    start_time = time.time()
    RPC.update(state="Idle", details="Not Quite Dead Yet.", large_image="afp32_big", large_text=f"Version {version} ({type})", start=start_time)