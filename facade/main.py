import os
import consul
from fastapi import FastAPI, status

import controller

c = consul.Consul(
    host=os.environ["CONSUL_IP"], 
    port=os.environ["CONSUL_PORT"]
)

c.agent.service.register(
    name=os.environ["SERVICE_NAME"],
    port=int(os.environ["SERVICE_PORT"]),
    address=os.environ["SERVICE_HOST"],
    service_id=f"{os.environ['SERVICE_NAME']}:{os.environ['SERVICE_PORT']}",
)

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['facade'], 
    prefix='/facade'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}
