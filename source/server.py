"""main server to listen to webhooks"""
import json
from typing import Dict, Any

from flask import Flask, request

app: Flask = Flask(__name__)

@app.route('/', methods=["POST"])
def recieve() -> None:
    """recieve data and pass it to update"""
    data: Dict[str, Any] = json.loads(request.data)
