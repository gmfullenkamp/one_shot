"""
Learning how to distribute code across threads.
"""
import threading
import time

# Capture program start time
start_time = time.perf_counter()

thread_pool = list()  # Container to hold threads
total_delay = 0

# Container with random int (5, 20)
delay_index = [5, 9, 13, 19, 16, 14, 7, 17]


# A worker method
def worker(delay: int) -> None:
    # Doing something
    time.sleep(delay)
    print(f"Worker_{delay} took {delay} secs to complete")


# Create worker threads and add them to thread_pool
for i in range(len(delay_index)):
    _delay = delay_index[i]
    total_delay += _delay
    t = threading.Thread(target=worker, name=f"Worker_{_delay}")  # TODO: Fix old thread worker delay bug
    thread_pool.append(t)

# Start worker threads
for _thread in thread_pool:
    _thread.start()
    print(f"--- Started {_thread.name}")

# Join the threads
duration_from_decorator = 0
for _thread in thread_pool:
    _thread.join()
    print(f"--- Completed {_thread.name}")
    print(f"{_thread.name} took {_thread.thread_duration} secs ")
    duration_from_decorator += _thread.thread_duration

# Capture program execuation time
end_time = time.perf_counter()
execution_time = end_time - start_time

# Print stats
print(f'Total execution time: {execution_time} secs')
print(f'Total no of threads: {len(thread_pool)}')
print(f'Average total time: {execution_time / len(thread_pool)}')
