import os
import random
import time
import dotenv
from websocket import create_connection


def worker():
    # Load environment variables
    dotenv.load_dotenv()
    WS_HOST = os.getenv("WS_HOST")
    AVG_TIME_BETWEEN_EVENTS_MS = int(os.getenv("AVG_TIME_BETWEEN_EVENTS_MS"))
    STD_DV_TIME_BETWEEN_EVENTS_MS = int(os.getenv("STD_DV_TIME_BETWEEN_EVENTS_MS"))

    print("Worker started")
    time.sleep(5)

    platform_bag = []

    if os.getenv("GITHUB_ENABLED").lower() == "true":
        print("GitHub enabled")
        platform_bag.append("github")
    if os.getenv("GITLAB_ENABLED").lower() == "true":
        print("GitLab enabled")
        platform_bag.append("gitlab")
    if os.getenv("AZURE_REPOS_ENABLED").lower() == "true":
        print("Azure Repos enabled")
        platform_bag.append("azure_repos")

    if os.getenv("GITHUB_ACTIONS_ENABLED").lower() == "true":
        print("GitHub Actions enabled")
        platform_bag.append("github_actions")

    if os.getenv("AZURE_PIPELINES_ENABLED").lower() == "true":
        print("Azure Pipelines enabled")
        platform_bag.append("azure_pipelines")

    while True:
        sleep_time = random.gauss(AVG_TIME_BETWEEN_EVENTS_MS, STD_DV_TIME_BETWEEN_EVENTS_MS) / 1000
        time.sleep(sleep_time)

        platform = random.choice(platform_bag)
        if platform == "github":
            ws_github = create_connection(f"ws://{WS_HOST}/events/ingestion/github/ws")
            # Add your GitHub specific code here

        """elif platform == "gitlab":
            # Add your GitLab specific code here

        elif platform == "azure_repos":
            # Add your Azure Repos specific code here

        elif platform == "github_actions":
            # Add your GitHub Actions specific code here

        elif platform == "azure_pipelines":
            # Add your Azure Pipelines specific code here
            """

    print("Worker finished")
