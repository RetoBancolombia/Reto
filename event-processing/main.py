import json
import os
import sys
from datetime import datetime, timezone
from typing import Annotated

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pymongo import MongoClient

from github import github_process
from mongodb_conn import MongoManager

"""
Define the processors for each event source
The value must be a function that receives the body of the message, and a mongo db
"""
processors_dict = {
    "github": github_process
}


def callback(channel, method, properties, body):
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
    print(f" [{datetime.now().isoformat()}] Received message")
    db = MongoManager.get_db_instance()
    try:
        processor = processors_dict[body["event_source"]]
        processor(body, db)
    except KeyError:
        print(f"[{datetime.now().isoformat()}] [WARN] Unsupported event source {body['event_source']}, ignoring message")
        return


def main():

    rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=pika.PlainCredentials("guest", "pass")
    ))
    rabbit_channel = rabbit_connection.channel()

    rabbit_channel.queue_declare(queue='events', durable=True)

    rabbit_channel.basic_consume(queue='events', on_message_callback=callback, auto_ack=True)

    print(f'[{datetime.now().isoformat()}] [INFO] Waiting for messages. To exit press CTRL+C')
    rabbit_channel.start_consuming()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)