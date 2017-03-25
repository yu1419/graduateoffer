from new_url import update_all
from update_offer import update_all_offer
import threading
import time
delay = 60*4


def update_data(update_time):
    while True:
        t1 = threading.Thread(target=update_all)
        t1.start()
        time.sleep(delay)
        t2 = threading.Thread(target=update_all_offer)
        t2.start()
        t1.join()
        t2.join()
        time.sleep(update_time)


if __name__ == "__main__":
    update_data(60*60*4)
