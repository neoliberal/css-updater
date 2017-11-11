"""manages github repos"""
import os
import tempfile

import pygit2 as git

from .webhook.handler import Handler
from .config_handler import ConfigHandler


class Manager(object):
    """handles git repos"""

    def __init__(self: Manager, handler: Handler) -> None:
        self.webhook_handler: Handler = handler
        self.temp_dir: tempfile.TemporaryDirectory = tempfile.TemporaryDirectory()
        self.repo: git.Repository = self.get_repo()
        self.config: ConfigHandler = self.get_config()

    def __del__(self: Manager) -> None:
        self.temp_dir.cleanup()

    def get_repo(self: Manager) -> git.Repository:
        """clone or initialize repository"""

        return git.clone_repository(
            self.webhook_handler.git_url, path=self.temp_dir.name)

    def get_config(self: Manager) -> ConfigHandler:
        """gets config file inside repo"""
        repo_index: git.repository.Index = self.repo.index
        repo_index.read()
        try:
            config_entry = repo_index["css_updator.json"]
        except KeyError:
            print("no config file exists")
        else:
            with self.repo[config_entry.id] as blob:
                return ConfigHandler(blob.data)
        return ConfigHandler("")
