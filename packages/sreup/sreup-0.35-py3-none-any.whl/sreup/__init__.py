import time,os
from sreup.common import config, utils, Requests
from sreup.ThreadMain import ThreadMain
arr_threads=[]
def start(thread_number=3):
    try:
        utils.clear_data()
        Requests.get(config.ServerAdress.REUP_SERVER + "client/start")
        for _ in range(thread_number):
            t = ThreadMain()
            t.start()
            arr_threads.append(t)
            time.sleep(1)
        for t in arr_threads:
            t.join(config.Timeout.THREAD)
    except:
        pass
    os.system("reboot")
