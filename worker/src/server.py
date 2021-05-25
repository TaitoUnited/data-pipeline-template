import threading
import time
from src.examples.continuous import main as continuous

threads = []

# Init threads
# NOTE: add your threads here
threads.append(threading.Thread(target=continuous, daemon=True))

# Start all threads
for thread in threads:
    thread.start()

# Exit if any of the threads exit
while all(thread.is_alive() for thread in threads):
    time.sleep(0.5)
