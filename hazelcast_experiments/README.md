
## To start the local cluster
```
# run this from the working directory
# each node can be launched from separate terminal
hz start -c hazelcast.yaml
```

## To run Hazerlcast Management Service
```
hz-mc start -Dhazelcast.mc.http.port=9000 
```

```
# to put thousand values into map
python put_thousand_elms.py

# then kill manually some nodes in the management service and look at the stats
```

```
# to count to 3000 in 3 seperate threads
python calc.py
```

```
# to produce 12 elements (produces 10 - which is the maxsize of the queue specified in the config - and then hangs)

python producer.py
```

```
# to consume those from two consumers:
python consumer.py
```