import tqdm
import threading
import subprocess
from sys import executable
from time import sleep

timeout = 90
rates = [0.25, 0.5, 1, 2, 5, 10, 25, 50, 100, 250, 500]


def run_thread(**kwargs):
    try:
        args = [executable, kwargs.get('task', 'sender.py'), '--rate', str(kwargs.get('rate', 1))]
        result = subprocess.run(args, timeout=kwargs.get('timeout', 60), capture_output=True)
    except subprocess.TimeoutExpired as e:
        pass


# время, которое работает процесс
local_timeout = 70
for rate in tqdm.tqdm(rates):
    thread_sender = threading.Thread(target=run_thread, kwargs={'task': 'sender.py', 'rate': rate, 'timeout': local_timeout+5})
    thread_sda = threading.Thread(target=run_thread, kwargs={'task': 'reciver.py', 'rate': rate, 'timeout': local_timeout})

    thread_sender.start()
    thread_sda.start()

    thread_sender.join(timeout)
    thread_sda.join(timeout)

    sleep(3)