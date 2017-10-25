"""main server to listen to webhooks"""
import json
from typing import Dict, Any, TypeVar

from flask import Flask, request, abort

# leave my typedefs alone, pylint: disable=C0103
Key = TypeVar("Key")
WebhookData = Dict[str, Key]

app: Flask = Flask(__name__)

def verify(git_hash: str, local_key: str) -> bool:
    """verifies that git string is the same as the local string"""
    import hmac
    from hashlib import sha1
    local_hash: str = "sha1=" + hmac.new(str.encode(local_key), digestmod=sha1).hexdigest()
    return hmac.compare_digest(git_hash, local_hash)

@app.route('/webhook', methods=["POST"])
def webhook() -> None:
    """recieve data and pass it to update"""
    if request.methods == "POST":
        if not verify(request.headers["X-Hub-Signature"], ""):
            abort(401)

        data: WebhookData[Any] = json.loads(request.data)
    else:
        abort(400)
