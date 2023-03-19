import hazelcast

from tqdm import tqdm

if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient()
    
    # Get the Distributed Map from Cluster.
    map = hz.get_map("tm").blocking()
    # Standard Put and Get
    for i in range(1000):
        map.put(i, "test")
    
    # Shutdown this Hazelcast Client
    hz.shutdown()
