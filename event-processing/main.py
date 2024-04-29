
import json
import os
import sys
import time
from datetime import datetime
from typing import Callable

import pika
import pymongo.database
from dotenv import load_dotenv

from providers.azure import azure_process

load_dotenv()
from providers.github import github_process
from providers.mongodb_conn import MongoManager


"""
Define the processors for each event source
The value must be a function that receives the body of the message, and a mongo db
"""
processors_dict: dict[str, Callable[[dict, pymongo.database.Database], None]] = {
    "github": github_process,
    "azure_pipelines": azure_process
}


def callback(channel, method, properties, raw_body):
    """
    Method to handle the messages received from the queue
    :param channel:
    :param method:
    :param properties:
    :param body:
    :return:
    """

    # data["event_timestamp"] = isoformat
    # data["event_source"] = "github"
    # data["event_type"] = websocket.headers.get("X-GitHub-Event")'
    print(f"[{datetime.now().isoformat()}] [INFO] Received message")
    db = MongoManager.get_db_instance()
    body = json.loads(raw_body)
    try:
        processor = processors_dict[body["event_source"]]
        processor(body, db)
    except KeyError:
        print(f"[{datetime.now().isoformat()}] [WARN] Unsupported event source {body['event_source']}, ignoring message")
        return


def main():
    rabbit_connection = None
    for i in range(15):
        print(f"Trying to connect to RabbitMQ, attempt {i}")

        try:
            rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.getenv("RABBIT_HOST", "localhost"),
                port=os.getenv("RABBIT_PORT", 5672),
                credentials=pika.PlainCredentials(os.getenv("RABBIT_USER", "guest"), os.getenv("RABBIT_PASS", "pass"))
            ))
            break
        except:
            print('Connection failed, retrying in 3s')
            # avoid rapid reconnection on longer RMQ server outage
            time.sleep(3)

    print("Connected to RabbitMQ")
    rabbit_channel = rabbit_connection.channel()

    rabbit_channel.queue_declare(queue='events', durable=True)

    rabbit_channel.basic_consume(queue='events', on_message_callback=callback, auto_ack=True)

    print(f'[{datetime.now().isoformat()}] [INFO] Waiting for messages. To exit press CTRL+C')
    rabbit_channel.start_consuming()



if __name__ == '__main__':
    try:
        print("Starting event-processing service")
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)