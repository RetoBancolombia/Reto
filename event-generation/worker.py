import datetime
import json
import os
import random
import time
import uuid

import dotenv
from faker import Faker
from websocket import create_connection

from providers.Azure import AzureProvider
from providers.github import GithubProvider


def worker():
    # Load environment variables
    dotenv.load_dotenv()
    WS_HOST = os.getenv("WS_HOST")
    AVG_TIME_BETWEEN_EVENTS_MS = int(os.getenv("AVG_TIME_BETWEEN_EVENTS_MS"))
    STD_DV_TIME_BETWEEN_EVENTS_MS = int(os.getenv("STD_DV_TIME_BETWEEN_EVENTS_MS"))

    config = {
        "WS_HOST": WS_HOST,
    }

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
        # Sleep for a random time
        sleep_time = random.gauss(AVG_TIME_BETWEEN_EVENTS_MS, STD_DV_TIME_BETWEEN_EVENTS_MS) / 1000
        time.sleep(sleep_time)

        # Choose a random platform
        platform = random.choice(platform_bag)
        if platform == "github":
            GithubProvider(config).generate()
        elif platform == "azure_pipelines":
            AzureProvider(config).generate()

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
