"""manages github repos"""
import git

class GitManager(object):
    """handles git repos"""
    def __init__(self: GitManager, master_branch: str = "master", test_branch: str = "development") -> None:
        self.master_branch = master_branch
        self.test_brach = test_branch
