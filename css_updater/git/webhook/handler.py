"""handles webhook"""
import os
from typing import Any, List, Dict, Tuple


class Handler(object):
    """wraps webhook data"""

    def __init__(self: Handler, data: Dict[str, Any]) -> None:
        self.data: Dict[str, Any] = data

    @property
    def head_commit(self: Handler) -> Dict[str, Any]:
        """returns head_commit for convienent access"""
        return self.data["head_commit"]

    @property
    def commits(self: Handler) -> List[Dict[str, Any]]:
        """returns commits"""
        return self.data["commits"]

    @property
    def repo_id(self: Handler) -> str:
        """returns repo's id"""
        return self.data["repository"]["id"]

    @property
    def timestamp(self: Handler) -> str:
        """returns timestamp of the head commit"""
        return self.head_commit["timestamp"]

    @property
    def changed_files(self: Handler) -> List[str]:
        """returns added or changed files"""
        added: List[str] = [commit["added"] for commit in self.commits]
        modified: List[str] = [commit["modified"] for commit in self.commits]
        return added + modified

    @property
    def removed_files(self: Handler) -> List[str]:
        """returns removed files"""
        return [commit["removed"] for commit in self.commits]

    @property
    def author(self: Handler) -> str:
        """returns author of head commit"""
        return self.head_commit["author"]["username"]

    @property
    def branch(self: Handler) -> str:
        """returns the branch the commit was pushed to"""
        return self.data["ref"].split('/')[-1]

    @property
    def git_url(self: Handler) -> str:
        """returns url to github repository"""
        return self.data["repository"]["git_url"]

    def changed_assets(self: Handler) -> Tuple[List[str], List[str]]:
        """
        identifies changed assets to upload or remove by checking if any changed files are images
        returns a tuple containing modified / new files and removed files
        """
        endings: List[str] = ["png", "jpg"]

        uploading_files: List[str] = [
            file for file in self.changed_files
            for ending in endings
            if os.path.splitext(file)[1] == ending
        ]

        removed_files: List[str] = [
            file for file in self.removed_files
            for ending in endings
            if os.path.splitext(file)[1] == ending
        ]
        return (uploading_files, removed_files)

    def changed_stylesheet(self: Handler) -> bool:
        """checks if any sass files have been changed"""
        endings: List[str] = ["scss", "css"]
        return any(
            os.path.splitext(file)[1] == ending
            for file in self.changed_files
            for ending in endings
        )
