"""
Minimal HTTP wrapper that makes the predict function behave like an OpenFaaS function.
OpenFaaS gateway calls POST / on this container and forwards the response.
"""
from flask import Flask, request, Response
from handler import handle

app = Flask(__name__)


class Event:
    def __init__(self, body: bytes):
        self.body = body


@app.post("/")
def invoke():
    event = Event(body=request.data)
    result = handle(event, context=None)
    return Response(
        result["body"],
        status=result["statusCode"],
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
