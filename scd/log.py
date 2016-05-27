from threading import Lock
import time
Logfile = "16core.log"
LogTime = None

LOG_LOCK = Lock()

def log(value):
    LOG_LOCK.acquire()
    t1 = time.time()
    t2 = None
    with open('logtime', 'r') as f:
        l = f.readlines()
        t2 = float(l[0])
    with open(Logfile,'a') as f:
        f.write(str(t1 - t2) +' ' + str(value) + '\n')
    LOG_LOCK.release()
