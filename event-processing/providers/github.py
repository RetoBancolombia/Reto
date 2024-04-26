import datetime

import pymongo
from bson import ObjectId


def github_process(body, db: pymongo.database.Database):
    """
    Method to handle the messages received from the queue
    :param body:
    :return:
    """
    if body["event_type"] == "push":
        print(f"[{datetime.datetime.now().isoformat()}] [DEBUG] Received push event from GitHub with \
timestamp {body['event_timestamp']}")

        raw_commits: list = body["commits"]
        commits = []
        for raw_commit in raw_commits:
            commit = {
                "id": raw_commit["id"],
                "timestamp": datetime.datetime.fromisoformat(raw_commit["timestamp"]),
                "event_source": "github",
                "repository_id": body["repository"]["id"],
                "raw_commit": raw_commit
            }
            commits.append(commit)
        db.commits.insert_many(commits, ordered=False)
    elif body["event_type"] == "pull_request":
        print(f"[{datetime.datetime.now().isoformat()}] [DEBUG] Received pull_request event from GitHub with \
timestamp {body['event_timestamp']}")

        def get_date(date_str):
            if date_str is not None:
                return datetime.datetime.fromisoformat(date_str)
            return None

        pull_request = {
            "id": body["pull_request"]["id"],
            "created_at": get_date(body["pull_request"]["created_at"]),
            "updated_at": get_date(body["pull_request"]["updated_at"]),
            "closed_at": get_date(body["pull_request"]["closed_at"]),
            "merged_at": get_date(body["pull_request"]["merged_at"]),
            "event_source": "github",
            "action": body["action"],
            "repository_id": body["repository"]["id"],
            "raw_event": body
        }
        db.pullrequests.insert_one(pull_request)
