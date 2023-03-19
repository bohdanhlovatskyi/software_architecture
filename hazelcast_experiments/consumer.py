import hazelcast
import multiprocessing as mp

from time import sleep

def read_from_queue(consumer_name: str, q_to_write: mp.Queue) -> None:
    hz = hazelcast.HazelcastClient()
    q = hz.get_queue("queue").blocking()

    while True:
        item = q.take()
        # sleep(1e-3)
        q_to_write.put_nowait((consumer_name, item))

if __name__ == "__main__":
    ctx = mp.get_context('spawn')
    rq = mp.Queue(20)

    first_consumer = ctx.Process(target=read_from_queue, args=("first_consumer", rq))
    second_consumer = ctx.Process(target=read_from_queue, args=("second_consumer", rq))
    second_consumer.start()
    first_consumer.start()

    for i in range(12):
        print(rq.get())

    second_consumer.join()
    first_consumer.join()
