
## How to run

```shell

# add all the needed info
consul agent -dev
sh init_counsil.sh

# start local hazelcast cluster
hz-start # NOTE: do this three times from three different terminals or run in background

# start kafka server
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
kafka-server-start /usr/local/etc/kafka/server.properties
```


```shell
# start facade instance
cd facade
source env/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 --env-file .env
```

```shell
# from several terminals
cd logging
source env/bin/activate
python main --port <port>
```


```shell
# from several terminals
cd message
source env/bin/activate
python main --port <port>
```
