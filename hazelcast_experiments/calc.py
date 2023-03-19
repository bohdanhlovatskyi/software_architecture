import hazelcast

from time import (
    time, 
    sleep
)
import multiprocessing as mp

KEY = "var"
NUM_CLIENTS = 3
WTIME = 3 / 1e4
ITERS = 1000

def without_lock():
    hz = hazelcast.HazelcastClient()
    map = hz.get_map("map").blocking()

    for _ in range(ITERS):
        val = map.get(KEY)
        sleep(WTIME)
        val += 1
        map.put(KEY, val)

    hz.shutdown()

def with_pessimistic_lock():
    hz = hazelcast.HazelcastClient()
    map = hz.get_map("map").blocking()

    for _ in range(ITERS):
        map.lock(KEY)
        try:
            val = map.get(KEY)
            sleep(WTIME)
            val += 1
            map.put(KEY, val)
        finally:
            map.unlock(KEY)

    hz.shutdown()

def with_optimistic_lock():
    hz = hazelcast.HazelcastClient()
    map = hz.get_map("map").blocking()

    for _ in range(ITERS):
        while True:
            val = map.get(KEY)
            new_val = val
            sleep(WTIME)
            new_val += 1
            if map.replace_if_same(KEY, val, new_val):
                break

    hz.shutdown()

if __name__ == "__main__":
    approaches = [with_pessimistic_lock, with_optimistic_lock, without_lock]
   
    ctx = mp.get_context('spawn')

    processes = []
    for apr in approaches:
        print(apr.__name__)
        print("Refreshing the original value... ")
        hz = hazelcast.HazelcastClient()
        map = hz.get_map("map").blocking()
        map.put(KEY, 0)
        print("Original value refreshed... ")

        processes = []
        start_time = time()
        for idx in range(NUM_CLIENTS):
            p = ctx.Process(target=apr, args=())
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        print("Time taken: ", time() - start_time)
        print(map.get(KEY))
        hz.shutdown()
        print()
