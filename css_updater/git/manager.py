"""manages github repos"""
import os
from typing import Optional

import git

from .webhook.handler import Handler


class Manager(object):
    """handles git repos"""

    def __init__(self: Manager, handler: Handler, master: str = "master", test: str = "development") -> None:
        self.webhook_handler: Handler = handler
        self.master_branch: str = master
        self.test_branch: str = test
        self.repo: Optional[git.Repo] = None

    def initialize_repo(self: Manager) -> None:
        """clone or initialize repository"""

        directory = os.path.join(os.getcwd(), "repo")
        if os.path is not os.path.isdir(directory):
            os.makedirs(directory)
            self.repo = git.Repo.clone_from(
                self.webhook_handler.git_url, to_path=os.getcwd())
        else:
            # I"m going to assume the repo has already been created
            # dangerous assumption, and it'll bite me in the ass someday
            self.repo = git.Repo(path=directory)
        return

    def update_branch(self: Manager) -> None:
        """update the branch to reflect webhook data"""
        branch: str = self.webhook_handler.branch

