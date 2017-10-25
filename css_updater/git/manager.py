"""manages github repos"""
import git

from .webhook.handler import Handler

class Manager(object):
    """handles git repos"""
    def __init__(self: Manager, handler: Handler, master: str = "master", test: str = "development") -> None:
        self.webhook_handler: Handler = handler 
        self.master_branch = master
        self.test_brach = test
