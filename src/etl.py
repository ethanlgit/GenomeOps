
import time
import threading

from load import load
from transform import transform
from s3 import download_from_s3, upload_to_s3

from dotenv import load_dotenv
import os



# ***RUN FROM GenomeOps ROOT



load_dotenv()
postgres_password = os.getenv("POSTGRES_PASSWORD")
file_path = "data/raw/variant_summary.txt"

bucket_name = "genomeops-clinvar-0801"
s3_key = "raw/variant_summary.txt"


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

    download_from_s3(bucket_name, s3_key, file_path)
    df = transform(file_path)

    # OPTIONAL, EXPERIMENTAL
    # upload_to_s3(file_path, bucket_name, s3_key)

    load(df=df, pg_password=postgres_password)
    # --------------------------------------------------------------------------
    
    stop_event.set()
    timer_thread.join()

    elapsed = time.perf_counter() - start

    print(f"\rETL completed in {elapsed:.2f} seconds")
