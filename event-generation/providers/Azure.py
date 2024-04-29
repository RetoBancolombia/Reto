import json
import random

import faker
from faker import Faker
from websocket import create_connection

from providers.generator import Generator

fake = Faker()


class AzureProvider(Generator):
    def __init__(self, config):
        super().__init__(config)

    def generate(self):
        result_type: str = random.choices(["Succeeded", "Failed"],
                                          weights=[1, 1], k=1)[0]
        print(f"Generating azure pipeline event: ${result_type}")
        ws_azure = create_connection(f"ws://{self.config["WS_HOST"]}/events/ingestion/azure/ws")
        body = {
            "subscriptionId": fake.uuid4(),
            "notificationId": random.randint(1, 1000000),
            "id": fake.uuid4(),
            "eventType": "ms.vss-pipelines.job-state-changed-event",
            "publisherId": "pipelines",
            "message":
                {
                    "text": f"Run 20221121.5 stage Build job Compile ${result_type}.",
                    "html": f"Run 20221121.5 stage Build job <a href=\"https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/results?buildId=2710088\">Compile</a> ${result_type}.",
                    "markdown": f"Run 20221121.5 stage Build job [Compile](https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/results?buildId=2710088) ${result_type}."
                },
            "detailedMessage":
                {
                    "text": f"Run 20221121.5 stage Build job Compile ${result_type}.",
                    "html": f"Run 20221121.5 stage Build job <a href=\"https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/results?buildId=2710088\">Compile</a> ${result_type}.",
                    "markdown": f"Run 20221121.5 stage Build job [Compile](https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/results?buildId=2710088) ${result_type}."
                },
            "resource":
                {
                    "job":
                        {
                            "_links":
                                {
                                    "web":
                                        {
                                            "href": "https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/results?buildId=2"
                                        },
                                    "pipeline.web":
                                        {
                                            "href": "https://dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_build/definition?definitionId=2"
                                        }
                                },
                            "id": "00000000-0000-0000-0000-000000000000",
                            "name": "__default",
                            "state": "completed",
                            "result": result_type.lower(),
                            "startTime": "2022-11-21T16:42:52.7761408Z",
                            "finishTime": "2022-11-21T16:42:52.7761408Z"
                        },
                    "stage":
                        {
                            "id": "00000000-0000-0000-0000-000000000000",
                            "name": "__default",
                            "displayName": None,
                            "state": "completed",
                            "result": result_type.lower(),
                            "startTime": None,
                            "finishTime": None
                        },
                    "run":
                        {
                            "pipeline":
                                {
                                    "url": "https://codedev.ms/org/091d79ee-dc21-465e-86a2-b4006b9d0921/_apis/Pipelines/2?revision=2",
                                    "id": 2,
                                    "revision": 2,
                                    "name": "TEST-CI",
                                    "folder": "\\"
                                },
                            "state": "completed",
                            "result": result_type.lower(),
                            "createdDate": "2022-11-21T16:42:52.7761408Z",
                            "finishedDate": "2022-11-21T16:42:52.7761408Z",
                            "id": 2,
                            "name": "2"
                        },
                    "pipeline":
                        {
                            "url": "https://codedev.ms/org/091d79ee-dc21-465e-86a2-b4006b9d0921/_apis/Pipelines/2?revision=2",
                            "id": 2,
                            "revision": 2,
                            "name": "TEST-CI",
                            "folder": "\\"
                        },
                    "repositories":
                        [
                            {
                                "type": "Git",
                                "change":
                                    {
                                        "author":
                                            {
                                                "name": "Fabrikam John",
                                                "email": "john@fabrikamfiber.com",
                                                "date": "2022-11-11T15:09:21Z"
                                            },
                                        "committer":
                                            {
                                                "name": "Fabrikam John",
                                                "email": "john@fabrikamfiber.com",
                                                "date": "2022-11-11T15:09:21Z"
                                            },
                                        "message": "Added Viva support"
                                    },
                                "url": "https://fabrikamfiber@dev.azure.com/fabrikamfiber/fabrikamfiber-viva/_git/fabrikamfiber"
                            },
                            {
                                "type": "GitHub",
                                "change":
                                    {
                                        "author":
                                            {
                                                "name": "Fabrikam John",
                                                "email": "john@github.com",
                                                "date": "2022-08-11T15:05:20Z"
                                            },
                                        "committer":
                                            {
                                                "name": "Fabrikam John",
                                                "email": "john@github.com",
                                                "date": "2022-08-11T15:05:20Z"
                                            },
                                        "message": "Added Viva open source REST API library"
                                    },
                                "url": "https://api.github.com/repos/FabrikamFiber/Viva"
                            }
                        ]
                },
            "resourceVersion": "5.1-preview.1",
            "resourceContainers":
                {
                    "collection":
                        {
                            "id": "c12d0eb8-e382-443b-9f9c-c52cba5014c2"
                        },
                    "account":
                        {
                            "id": "f844ec47-a9db-4511-8281-8b63f4eaf94e"
                        },
                    "project":
                        {
                            "id": "be9b3917-87e6-42a4-a549-2bc06a7a878f"
                        }
                },
            "createdDate": "2022-11-21T16:42:53.5254422Z"
        }
        ws_azure.send(json.dumps(body))
        ws_azure.close()
