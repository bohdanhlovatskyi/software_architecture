#!/bin/bash

# consul agent -dev
consul kv put HAZELCAST_CLUSTER_NAME hz
consul kv put HAZELCAST_MAP_NAME logging_map
consul kv put KAFKA_TOPIC message
consul kv put KAFKA_INSTANCE localhost:9092
consul kv put KAFKA_CONSUMER_GROUP message_group
