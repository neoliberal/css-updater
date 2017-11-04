"""handles webhook"""
from typing import Any, List, Dict


class Handler(object):
    """wraps webhook data"""

    def __init__(self: Handler, data: Dict[str, Any]) -> None:
        self.data: Dict[str, Any] = data

    @property
    def head_commit(self: Handler) -> Dict[str, Any]:
        """returns head_commit for convienent access"""
        return self.data["head_commit"]

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
        return self.head_commit["added"] + self.head_commit["modified"]

    @property
    def removed_files(self: Handler) -> List[str]:
        """returns removed files"""
        return self.head_commit["removed"]

    @property
    def commits(self: Handler) -> List[Dict[str, Any]]:
        """returns commits"""
        return self.data["commits"]

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
