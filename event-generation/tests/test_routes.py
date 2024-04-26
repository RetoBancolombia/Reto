from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from main import app  # assuming your FastAPI app is named "app" in "main.py"
import json

client = TestClient(app)

def test_ping_endpoint():
    response = client.get("/events/ingestion/ping")
    assert response.status_code == 200
    assert response.json() == "pong"
    assert response.headers["content-type"] == "application/json"

def test_websocket():
    """
    Test the websocket endpoint with a correct github event
    """
    headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Hookshot/300dae6",
            "X-GitHub-Delivery": "44c57454-0136-11ef-8f7d-dcbb57f14c86",
            "X-GitHub-Event": "push",
            "X-GitHub-Hook-ID": "474170556",
            "X-GitHub-Hook-Installation-Target-ID": "167820875",
            "X-GitHub-Hook-Installation-Target-Type": "organization",
    }
    with client.websocket_connect("/events/ingestion/github/ws", headers=headers) as websocket:
        msg = websocket.receive_text()
        assert msg == "Accepted event type"
        request_body = json.load(open("../examples/commit-push.json"))[1]
        try:
            websocket.send_json(request_body)
        except WebSocketDisconnect:
            pass

def test_websocket_ignore():
    """
        Test the websocket endpoint with an incorrect github event
        """
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "GitHub-Hookshot/300dae6",
        "X-GitHub-Delivery": "44c57454-0136-11ef-8f7d-dcbb57f14c86",
        "X-GitHub-Event": "repository",
        "X-GitHub-Hook-ID": "474170556",
        "X-GitHub-Hook-Installation-Target-ID": "167820875",
        "X-GitHub-Hook-Installation-Target-Type": "organization",
    }
    with client.websocket_connect("/events/ingestion/github/ws", headers=headers) as websocket:
        msg = websocket.receive_text()
        assert msg == "Ignored event type"
