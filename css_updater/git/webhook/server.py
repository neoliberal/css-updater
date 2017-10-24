"""main server to listen to webhooks"""
import json
from typing import Dict, Any, TypeVar

from flask import Flask, request, abort

# leave my typedefs alone, pylint: disable=C0103
Key = TypeVar("Key")
WebhookData = Dict[str, Key]

app: Flask = Flask(__name__)

@app.route('/webhook', methods=["POST"])
def webhook() -> None:
    """recieve data and pass it to update"""
    if request.methods == "POST":
        data: WebhookData[Any] = json.loads(request.data)
    else:
        abort(400)
