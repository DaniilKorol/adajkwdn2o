import requests, time, random, re
import threading

def generation():
    response = requests.get(f'http://90.156.215.72:8234')

time.sleep(5)
threads = []
for i in range(1600):
    thread = threading.Thread(target=generation)
    thread.start()
    threads.append(thread)

# Дождаться окончания всех потоков
for thread in threads:
    thread.join()

