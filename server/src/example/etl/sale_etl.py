import time
from ..daos import sale_dao


def listen():
    while True:
        print("Example implementation that just keeps on running.")
        time.sleep(60)


def extract():
    print("Example implementation that runs once.")
