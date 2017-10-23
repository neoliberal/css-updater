"""updates subreddit css with compiled sass"""
from os import path
from typing import List, Dict, Any, Tuple

import praw
import sass

# leave my typedefs alone, pylint: disable=C0103
WebhookResponse = Dict[str, Any]


class SubredditUploader(object):
    """various uploads"""

    def __init__(
            self: SubredditUploader, data: WebhookResponse,
            absolute_path: str, reddit: praw.Reddit, subreddit: str
    ) -> None:
        self.webhook: WebhookResponse = data
        self.reddit: praw.Reddit = reddit
        self.subreddit: str = subreddit
        self.path: str = absolute_path

    def changed_assets(self: SubredditUploader) -> Tuple[List[str], List[str]]:
        """
        identifies changed assets to upload or remove by checking if any changed files are images
        returns a tuple containing modified / new files and removed files
        """
        endings: List[str] = ["png", "jpg"]

        head_commit: Dict[str, Any] = self.webhook["head_commit"]

        uploading_files: List[str] = [
            file for file in (head_commit["modified"] + head_commit["added"])
            for ending in endings
            if path.splitext(file)[1] == ending
        ]

        # removed_files require a name, not file extension
        removed_files: List[str] = [
            path.splitext(file)[0] for file in head_commit["removed"]
            for ending in endings
            if path.splitext(file)[1] == ending
        ]
        return (uploading_files, removed_files)

    def upload_stylesheet(self: SubredditUploader) -> bool:
        """compiles and uploads stylesheet"""
        style: str = ""
        try:
            style = sass.compile(
                filename=(self.path + "index.scss"), output_style="compressed")
        except sass.CompileError as sass_error:
            print(sass_error)
            return False

        self.reddit.subreddit(self.subreddit).stylesheet.update(style)
        return True

    def changed_stylesheet(self: SubredditUploader) -> bool:
        """checks if any sass files have been changed"""
        ending: str = "scss"
        head_commit: Dict[str, Any] = self.webhook["head_commit"]
        return any(
            path.splitext(file)[1] == ending
            for file in (head_commit["modified"] + head_commit["added"])
        )
