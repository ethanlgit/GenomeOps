
import time
import threading

from load import load
from transform import transform

from dotenv import load_dotenv
import os


load_dotenv()
postgres_password = os.getenv("POSTGRES_PASSWORD")
file_path = "data/raw/variant_summary.txt"



def timer(stop_event):
    seconds = 0

    while not stop_event.wait(1):
        seconds += 1
        print(f"\rElapsed Time: {seconds}s", end="", flush=True)


#     Main worker                Timer worker
#      │                          │
#      │                         work
#      │                          │
#      │                         work
#      │                          │
#      │── ".set()" ─────────────>│
#      │                          |
#    .join()                      │
# halts main thread            finishes
#      │                          │
#      │<─────── done ────────────│
#      │
#      ▼
# continue

if __name__ == "__main__":

    stop_event = threading.Event()

    start = time.perf_counter()

    timer_thread = threading.Thread(target=timer, args=(stop_event,))
    timer_thread.start()


    # --------------------------------------------------------------------------
    df = transform(file_path)
    load(df=df, pg_password=postgres_password)
    # --------------------------------------------------------------------------
    
    stop_event.set()
    timer_thread.join()

    elapsed = time.perf_counter() - start

    print(f"\rETL completed in {elapsed:.2f} seconds")
