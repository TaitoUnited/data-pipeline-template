import time
import threading
from src.example.services import sale_etl_service


def add_thread(threads, target, daemon=True):
    threads.append(threading.Thread(target=target, daemon=daemon))


def get_worker_threads():
    threads = []

    # -----------------------------------------------------------------------
    # NOTE: Add your worker threads here. They will be executed continuously.
    # -----------------------------------------------------------------------
    add_thread(threads, sale_etl_service.listen)

    return threads


def start_worker(wait=False):
    # Start all threads
    threads = get_worker_threads()
    for thread in threads:
        thread.start()

    if wait:
        # Exit if any of the threads exit
        while all(thread.is_alive() for thread in threads):
            time.sleep(0.5)
        exit(1)
