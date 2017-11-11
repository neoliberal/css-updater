"""manages github repos"""
import os
import tempfile
from typing import Dict, Any

import pygit2 as git

from .webhook.handler import Handler


class Manager(object):
    """handles git repos"""

    def __init__(self: Manager, handler: Handler) -> None:
        self.webhook_handler: Handler = handler
        self.temp_dir: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory()
        self.repo: git.Repository = git.clone_repository(
            self.webhook_handler.git_url, path=self.temp_dir.name)

        with open(os.path.join(self.temp_dir.name, "css-updater.json")) as config:
            import json
            self.config: Dict[str, Any] = json.loads(config.read())

    def __del__(self: Manager) -> None:
        self.temp_dir.cleanup()
