import hazelcast

from time import (
    time, 
)
import multiprocessing as mp


if __name__ == "__main__":

    hz = hazelcast.HazelcastClient()

    q = hz.get_queue("queue").blocking()
    q.clear()

    for i in range(12):
        print(f"Putting {i}-th element. Capacity left: ", q.remaining_capacity())
        q.put(i)
    hz.shutdown()
