import datetime
import json
import os
import random
import time
import uuid

import dotenv
from faker import Faker
from websocket import create_connection

fake = Faker()
def generate_github_commit():
    return {
        "id": os.urandom(10).hex(),
        "tree_id": os.urandom(10).hex(),
        "distinct": True,
        "message": fake.sentence(),
        "timestamp": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=random.randint(0, 60 * 12))).isoformat(),
        "url": "https://github.com/RetoBancolombia/Reto/commit/40e200b007313b55c2d82fbf713a02d7be19a8d7",
        "author": {
            "name": "Diego Granada M",
            "email": "diegogranada7@gmail.com",
            "username": "coldblade2000"
        },
        "committer": {
            "name": "Diego Granada M",
            "email": "diegogranada7@gmail.com",
            "username": "coldblade2000"
        },
        "added": [
            "event-ingestion/.idea/.gitignore",
            "event-ingestion/.idea/event-ingestion.iml",
            "event-ingestion/.idea/inspectionProfiles/profiles_settings.xml",
            "event-ingestion/.idea/misc.xml",
            "event-ingestion/.idea/modules.xml",
            "event-ingestion/.idea/vcs.xml",
            "event-ingestion/main.py"
        ],
        "removed": [],
        "modified": []
    }


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
        # Sleep for a random time
        sleep_time = random.gauss(AVG_TIME_BETWEEN_EVENTS_MS, STD_DV_TIME_BETWEEN_EVENTS_MS) / 1000
        time.sleep(sleep_time)

        # Choose a random platform
        platform = random.choice(platform_bag)
        if platform == "github":
            type = random.choices(["push", "pull_request.opened", "pull_request.closed"],
                                  weights=[0.6, 0.25, 0.15], k=1)
            if type[0] == "push":
                ws_github = create_connection(f"ws://{WS_HOST}/events/ingestion/github/ws",
                                              header={
                                                  "Accept": "*/*",
                                                  "Content-Type": "application/json",
                                                  "User-Agent": "GitHub-Hookshot/300dae6",
                                                  "X-GitHub-Delivery": str(uuid.uuid4()),
                                                  "X-GitHub-Event": "push",
                                                  "X-GitHub-Hook-ID": "474170556",
                                                  "X-GitHub-Hook-Installation-Target-ID": "167820875",
                                                  "X-GitHub-Hook-Installation-Target-Type": "organization"
                                              })
                commits = [generate_github_commit() for _ in range(1, 12)]
                body = {
                    "ref": "refs/heads/develop",
                    "before": "0cc1a68aeeb011721adbfc92faecfb6d481bc284",
                    "after": "40e200b007313b55c2d82fbf713a02d7be19a8d7",
                    "repository": {
                        "id": 790463501,
                        "node_id": "R_kgDOLx2EDQ",
                        "name": "Reto",
                        "full_name": "RetoBancolombia/Reto",
                        "private": True,
                        "owner": {
                            "name": "RetoBancolombia",
                            "email": None,
                            "login": "RetoBancolombia",
                            "id": 167820875,
                            "node_id": "O_kgDOCgC-Sw",
                            "avatar_url": "https://avatars.githubusercontent.com/u/167820875?v=4",
                            "gravatar_id": "",
                            "url": "https://api.github.com/users/RetoBancolombia",
                            "html_url": "https://github.com/RetoBancolombia",
                            "followers_url": "https://api.github.com/users/RetoBancolombia/followers",
                            "following_url": "https://api.github.com/users/RetoBancolombia/following{/other_user}",
                            "gists_url": "https://api.github.com/users/RetoBancolombia/gists{/gist_id}",
                            "starred_url": "https://api.github.com/users/RetoBancolombia/starred{/owner}{/repo}",
                            "subscriptions_url": "https://api.github.com/users/RetoBancolombia/subscriptions",
                            "organizations_url": "https://api.github.com/users/RetoBancolombia/orgs",
                            "repos_url": "https://api.github.com/users/RetoBancolombia/repos",
                            "events_url": "https://api.github.com/users/RetoBancolombia/events{/privacy}",
                            "received_events_url": "https://api.github.com/users/RetoBancolombia/received_events",
                            "type": "Organization",
                            "site_admin": False
                        },
                        "html_url": "https://github.com/RetoBancolombia/Reto",
                        "description": None,
                        "fork": False,
                        "url": "https://github.com/RetoBancolombia/Reto",
                        "forks_url": "https://api.github.com/repos/RetoBancolombia/Reto/forks",
                        "keys_url": "https://api.github.com/repos/RetoBancolombia/Reto/keys{/key_id}",
                        "collaborators_url": "https://api.github.com/repos/RetoBancolombia/Reto/collaborators{/collaborator}",
                        "teams_url": "https://api.github.com/repos/RetoBancolombia/Reto/teams",
                        "hooks_url": "https://api.github.com/repos/RetoBancolombia/Reto/hooks",
                        "issue_events_url": "https://api.github.com/repos/RetoBancolombia/Reto/issues/events{/number}",
                        "events_url": "https://api.github.com/repos/RetoBancolombia/Reto/events",
                        "assignees_url": "https://api.github.com/repos/RetoBancolombia/Reto/assignees{/user}",
                        "branches_url": "https://api.github.com/repos/RetoBancolombia/Reto/branches{/branch}",
                        "tags_url": "https://api.github.com/repos/RetoBancolombia/Reto/tags",
                        "blobs_url": "https://api.github.com/repos/RetoBancolombia/Reto/git/blobs{/sha}",
                        "git_tags_url": "https://api.github.com/repos/RetoBancolombia/Reto/git/tags{/sha}",
                        "git_refs_url": "https://api.github.com/repos/RetoBancolombia/Reto/git/refs{/sha}",
                        "trees_url": "https://api.github.com/repos/RetoBancolombia/Reto/git/trees{/sha}",
                        "statuses_url": "https://api.github.com/repos/RetoBancolombia/Reto/statuses/{sha}",
                        "languages_url": "https://api.github.com/repos/RetoBancolombia/Reto/languages",
                        "stargazers_url": "https://api.github.com/repos/RetoBancolombia/Reto/stargazers",
                        "contributors_url": "https://api.github.com/repos/RetoBancolombia/Reto/contributors",
                        "subscribers_url": "https://api.github.com/repos/RetoBancolombia/Reto/subscribers",
                        "subscription_url": "https://api.github.com/repos/RetoBancolombia/Reto/subscription",
                        "commits_url": "https://api.github.com/repos/RetoBancolombia/Reto/commits{/sha}",
                        "git_commits_url": "https://api.github.com/repos/RetoBancolombia/Reto/git/commits{/sha}",
                        "comments_url": "https://api.github.com/repos/RetoBancolombia/Reto/comments{/number}",
                        "issue_comment_url": "https://api.github.com/repos/RetoBancolombia/Reto/issues/comments{/number}",
                        "contents_url": "https://api.github.com/repos/RetoBancolombia/Reto/contents/{+path}",
                        "compare_url": "https://api.github.com/repos/RetoBancolombia/Reto/compare/{base}...{head}",
                        "merges_url": "https://api.github.com/repos/RetoBancolombia/Reto/merges",
                        "archive_url": "https://api.github.com/repos/RetoBancolombia/Reto/{archive_format}{/ref}",
                        "downloads_url": "https://api.github.com/repos/RetoBancolombia/Reto/downloads",
                        "issues_url": "https://api.github.com/repos/RetoBancolombia/Reto/issues{/number}",
                        "pulls_url": "https://api.github.com/repos/RetoBancolombia/Reto/pulls{/number}",
                        "milestones_url": "https://api.github.com/repos/RetoBancolombia/Reto/milestones{/number}",
                        "notifications_url": "https://api.github.com/repos/RetoBancolombia/Reto/notifications{?since,all,participating}",
                        "labels_url": "https://api.github.com/repos/RetoBancolombia/Reto/labels{/name}",
                        "releases_url": "https://api.github.com/repos/RetoBancolombia/Reto/releases{/id}",
                        "deployments_url": "https://api.github.com/repos/RetoBancolombia/Reto/deployments",
                        "created_at": 1713828633,
                        "updated_at": "2024-04-22T23:30:36Z",
                        "pushed_at": 1713851805,
                        "git_url": "git://github.com/RetoBancolombia/Reto.git",
                        "ssh_url": "git@github.com:RetoBancolombia/Reto.git",
                        "clone_url": "https://github.com/RetoBancolombia/Reto.git",
                        "svn_url": "https://github.com/RetoBancolombia/Reto",
                        "homepage": None,
                        "size": 54,
                        "stargazers_count": 0,
                        "watchers_count": 0,
                        "language": None,
                        "has_issues": True,
                        "has_projects": True,
                        "has_downloads": True,
                        "has_wiki": False,
                        "has_pages": False,
                        "has_discussions": False,
                        "forks_count": 0,
                        "mirror_url": None,
                        "archived": False,
                        "disabled": False,
                        "open_issues_count": 0,
                        "license": None,
                        "allow_forking": False,
                        "is_template": False,
                        "web_commit_signoff_required": False,
                        "topics": [],
                        "visibility": "private",
                        "forks": 0,
                        "open_issues": 0,
                        "watchers": 0,
                        "default_branch": "main",
                        "stargazers": 0,
                        "master_branch": "main",
                        "organization": "RetoBancolombia",
                        "custom_properties": {}
                    },
                    "pusher": {
                        "name": "coldblade2000",
                        "email": "diegogranada7@gmail.com"
                    },
                    "organization": {
                        "login": "RetoBancolombia",
                        "id": 167820875,
                        "node_id": "O_kgDOCgC-Sw",
                        "url": "https://api.github.com/orgs/RetoBancolombia",
                        "repos_url": "https://api.github.com/orgs/RetoBancolombia/repos",
                        "events_url": "https://api.github.com/orgs/RetoBancolombia/events",
                        "hooks_url": "https://api.github.com/orgs/RetoBancolombia/hooks",
                        "issues_url": "https://api.github.com/orgs/RetoBancolombia/issues",
                        "members_url": "https://api.github.com/orgs/RetoBancolombia/members{/member}",
                        "public_members_url": "https://api.github.com/orgs/RetoBancolombia/public_members{/member}",
                        "avatar_url": "https://avatars.githubusercontent.com/u/167820875?v=4",
                        "description": None
                    },
                    "sender": {
                        "login": "coldblade2000",
                        "id": 1772063,
                        "node_id": "MDQ6VXNlcjE3NzIwNjM=",
                        "avatar_url": "https://avatars.githubusercontent.com/u/1772063?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/coldblade2000",
                        "html_url": "https://github.com/coldblade2000",
                        "followers_url": "https://api.github.com/users/coldblade2000/followers",
                        "following_url": "https://api.github.com/users/coldblade2000/following{/other_user}",
                        "gists_url": "https://api.github.com/users/coldblade2000/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/coldblade2000/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/coldblade2000/subscriptions",
                        "organizations_url": "https://api.github.com/users/coldblade2000/orgs",
                        "repos_url": "https://api.github.com/users/coldblade2000/repos",
                        "events_url": "https://api.github.com/users/coldblade2000/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/coldblade2000/received_events",
                        "type": "User",
                        "site_admin": False
                    },
                    "created": False,
                    "deleted": False,
                    "forced": False,
                    "base_ref": None,
                    "compare": "https://github.com/RetoBancolombia/Reto/compare/0cc1a68aeeb0...40e200b00731",
                    "commits": commits,
                    "head_commit": commits[0]
                }
                ws_github.send(json.dumps(body))
                ws_github.close()

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
