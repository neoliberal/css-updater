"""handles secret files"""
import json
from typing import Dict, Any


class Secrets(object):
    """singleton model for holding secrets and returning them"""
    with open("secrets.json") as file:
        internal: Dict[str, Any] = json.loads(file.read())

    def __call__(self: Secrets) -> Dict[str, Any]:
        return self.internal
