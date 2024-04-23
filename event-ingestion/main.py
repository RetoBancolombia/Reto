import json
from datetime import datetime, timezone
from typing import Annotated

import pika
from fastapi import FastAPI, WebSocket, Depends
from pika.adapters.blocking_connection import BlockingChannel
from starlette.websockets import WebSocketDisconnect

app = FastAPI(
    title="GitHub Events Ingestion Microservice",
    description="This is a microservice to ingest events from GitHub and store them in a RabbitMQ queue",
    summary="GitHub Events Ingestion Microservice",
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


async def queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=pika.PlainCredentials("guest", "pass")
    ))
    channel = connection.channel()
    channel.queue_declare(queue='events', durable=True)
    try:
        yield channel
    finally:
        connection.close()


@app.get("/events/ingestion/")
async def root():
    return {"message": "Hello World"}


@app.get("/events/ingestion/ping")
async def say_hello():
    return "pong"


@app.websocket("/events/ingestion/github/ws")
async def websocket_endpoint(websocket: WebSocket, channel: Annotated[BlockingChannel, Depends(queue)]):
    """
    Websocket endpoint to receive events from GitHub
    """
    await websocket.accept()
    while True:
        if websocket.headers.get("X-GitHub-Event") not in ["push", "pull_request"]:
            await websocket.send_text("Ignored event type")
            return
        else:
            await websocket.send_text("Accepted event type")
        data = await websocket.receive_json()
        isoformat = datetime.now(timezone.utc).isoformat()
        data["timestamp"] = isoformat
        data["source"] = "github"
        channel.basic_publish(
            exchange='',
            routing_key='events',
            body=json.dumps(data)
        )
        print(f"[{isoformat}] Received event from GitHub of type {websocket.headers.get('X-GitHub-Event')}")

