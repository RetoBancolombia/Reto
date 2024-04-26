import multiprocessing
import time

import uvicorn
from fastapi import FastAPI

import worker

app = FastAPI(
    title="Repository event generation microservice",
    description="This is a microservice to generate events and send them through various webhooks",
    summary="Repository event generation microservice",
    version="0.1.0",
    contact={
        "name": "Diego Granada Martinez",
        "email": "diegogranada7@gmail.com"
    },
    license_info={
        "name": "Apache 2.0 with Commons Clause",
        "url": "https://commonsclause.com/"
    }
)


@app.get("/events/generation/")
async def root():
    return {"message": "Hello World"}



@app.get("/events/generation/ping")
async def ping():
    return "pong"

def server():
    uvicorn.run(app, host="localhost", port=3210, reload=True)



if __name__ == "__main__":
    # Runs server and worker in separate processes
    p1 = multiprocessing.Process(target=server)
    p1.start()

    time.sleep(1)  # Wait for server to start

    p2 = multiprocessing.Process(target=worker.worker)
    p2.start()

    p1.join()
    p2.join()