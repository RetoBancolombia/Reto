import datetime

import pymongo


def azure_process(body, db: pymongo.database.Database):
    """
    Method to handle the messages received from the queue
    :param body:
    :return:
    """
    print(f"[{datetime.datetime.now().isoformat()}] [DEBUG] Received event from Azure Pipelines with \
timestamp {body['event_timestamp']}")

    if body["eventType"] == "ms.vss-pipelines.job-state-changed-event":
        def get_date(date_str):
            if date_str is not None:
                return datetime.datetime.fromisoformat(date_str)
            return None

        pipeline_event = {
            "created_at": get_date(body["resource"]["run"]["createdDate"]),
            "finished_at": get_date(body["resource"]["run"]["finishedDate"]),
            "event_source": body["event_source"],
            "event_type": body["eventType"],
            "result": body["resource"]["run"]["result"],
            "pipeline_id": body["resource"]["run"]["pipeline"]["id"],
            "raw_event": body
        }
        db.pipelines.insert_one(pipeline_event)
