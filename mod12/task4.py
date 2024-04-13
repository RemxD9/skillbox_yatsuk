from threading import Thread, Lock
from queue import Queue
import time
import requests
from datetime import datetime


list_lock = Lock()


def get_timestamp():
    response = requests.get('http://127.0.0.1:8080/timestamp/{}'.format(int(time.time())))
    return response.text


def write_logs(filename, log_list):
    log_list.sort(key=lambda x: float(x[0]))
    with open(filename, 'w') as f:
        for timestamp, timestamp_str in log_list:
            f.write(f'{timestamp} {timestamp_str}\n')


def collect_logs(log_list):
    while True:
        timestamp = log_queue.get()
        if timestamp == 'DONE':
            break
        current_time = datetime.fromtimestamp(float(timestamp))
        log_list.append((timestamp, str(current_time)))


log_queue = Queue()
log_list = []

t = Thread(target=collect_logs, args=(log_list,))
t.start()

for _ in range(20):
    timestamp = time.time()
    log_queue.put(timestamp)
    time.sleep(1)

log_queue.put('DONE')

t.join()

write_logs('log.txt', log_list)
