import os
import consul
import uvicorn
import argparse
from fastapi import FastAPI, status

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import controller

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--port", help="port to run", required=True)
args = argParser.parse_args()

c = consul.Consul(
    host=os.environ["CONSUL_IP"], 
    port=os.environ["CONSUL_PORT"]
)

c.agent.service.register(
    name=os.environ["SERVICE_NAME"],
    port=int(args.port),
    address=os.environ["SERVICE_HOST"],
    service_id=f"{os.environ['SERVICE_NAME']}:{args.port}",
)

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['logging'], 
    prefix='/logging'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=int(args.port))
