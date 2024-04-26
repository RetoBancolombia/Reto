import multiprocessing
import time

import uvicorn
from fastapi import FastAPI

import worker
from providers.gitlab import get_fake_projects, get_fake_languages

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


@app.get("/gitlab/api/v4/projects")
async def list_gitlab_projects():
    return get_fake_projects()


@app.get("/gitlab/api/v4/projects/{p_id}/languages")
async def list_gitlab_projects(p_id: int):
    projects = get_fake_projects()

    project = next(x for x in projects if x["id"] == p_id)
    if len(project) > 0:
        return get_fake_languages(int(project["id"]))


def server():
    uvicorn.run(app, host="0.0.0.0", port=3210)


if __name__ == "__main__":
    # Runs server and worker in separate processes
    p1 = multiprocessing.Process(target=server)
    p1.start()

    time.sleep(1)  # Wait for server to start

    p2 = multiprocessing.Process(target=worker.worker)
    p2.start()

    p1.join()
    p2.join()
