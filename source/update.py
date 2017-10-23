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

    def upload_images(self: SubredditUploader, upload: List[str], delete: List[str]) -> bool:
        """uploads and deletes images"""
        stylesheet: praw.models.reddit.subreddit.SubredditStylesheet = (
            self.reddit.subreddit(self.subreddit).stylesheet
        )

        for file in upload:
            try:
                stylesheet.upload(path.splitext(file)[0], file)
            except praw.exceptions.APIException as upload_error:
                print(upload_error)
                return False

        for file in delete:
            try:
                stylesheet.delete_image(file)
            except praw.exceptions.APIException as delete_error:
                print(delete_error)
                return False

        return True

    def upload_reason(self: SubredditUploader) -> str:
        """creates upload reason"""
        head_commit: Dict[str, Any] = self.webhook["head_commit"]
        commit_id: str = head_commit["id"]
        timestamp: str = head_commit["timestamp"]
        author: str = head_commit["author"]["username"]
        return "Commit {1} created on {2} by {3}".format(commit_id, timestamp, author)

    def upload_stylesheet(self: SubredditUploader) -> bool:
        """compiles and uploads stylesheet"""
        style: str = ""
        try:
            style = sass.compile(
                filename=(self.path + "index.scss"), output_style="compressed")
        except sass.CompileError as sass_error:
            print(sass_error)
            return False

        try:
            self.reddit.subreddit(self.subreddit).stylesheet.update(
                style, reason=self.upload_reason())
        except praw.exceptions.APIException as reddit_error:
            print(reddit_error)
            return False

        return True

    def changed_stylesheet(self: SubredditUploader) -> bool:
        """checks if any sass files have been changed"""
        ending: str = "scss"
        head_commit: Dict[str, Any] = self.webhook["head_commit"]
        return any(
            path.splitext(file)[1] == ending
            for file in (head_commit["modified"] + head_commit["added"])
        )
