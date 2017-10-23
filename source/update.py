"""updates subreddit css with compiled sass"""
from os import path
from typing import List, Dict, Any, Tuple, Optional

import praw
import sass

# leave my typedefs alone, pylint: disable=C0103
WebhookResponse = Dict[str, Any]


class SubredditUploader(object):
    """various uploads"""

    # pylint: disable=R0913
    def __init__(
            self: SubredditUploader, data: WebhookResponse,
            absolute_path: str, reddit: praw.Reddit, subreddit: str, testing_subreddit: str
    ) -> None:
        self.webhook: WebhookResponse = data
        self.reddit: praw.Reddit = reddit
        self.path: str = absolute_path
        self.subreddit: praw.models.Subreddit = self.validate_subreddit(subreddit)
        self.testing_subreddit: Optional[praw.models.Subreddit] = (
            self.validate_subreddit(testing_subreddit))
        self.testable: bool = bool(testing_subreddit)

    def validate_subreddit(self: SubredditUploader,
                           subreddit: str) -> Optional[praw.models.Subreddit]:
        """validate that subreddits exist"""
        try:
            validated: praw.models.Subreddit = self.reddit.subreddit(subreddit)
        except praw.exceptions.APIException as praw_error:
            print(praw_error)
            return None
        else:
            return validated

    def get_subreddit_test(self: SubredditUploader, test: bool) -> praw.models.Subreddit:
        """gets appropriate subreddit based on if testing and if test sub is defined"""
        return self.subreddit if not(self.testable and test) else self.testing_subreddit

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

        removed_files: List[str] = [
            file for file in head_commit["removed"]
            for ending in endings
            if path.splitext(file)[1] == ending
        ]
        return (uploading_files, removed_files)

    def upload_images(self: SubredditUploader, upload: List[str],
                      delete: List[str], test: bool = False) -> bool:
        """uploads and deletes images"""
        subreddit = self.get_subreddit_test(test)
        stylesheet: praw.models.reddit.subreddit.SubredditStylesheet = subreddit.stylesheet

        for file in upload:
            try:
                stylesheet.upload(path.splitext(file)[0], file)
            except praw.exceptions.APIException as upload_error:
                print(upload_error)
                return False

        for file in delete:
            try:
                stylesheet.delete_image(path.splitext(file)[0])
            except praw.exceptions.APIException as delete_error:
                print(delete_error)
                return False

        return True

    def upload_reason(self: SubredditUploader, test: bool = False) -> str:
        """creates upload reason"""
        head_commit: Dict[str, Any] = self.webhook["head_commit"]
        warn: str = "" if not (test and self.testable) else "[Test] "
        commit_id: str = head_commit["id"]
        timestamp: str = head_commit["timestamp"]
        author: str = head_commit["author"]["username"]
        return "{1}Commit {2} created on {3} by {4}".format(warn, commit_id, timestamp, author)

    def changed_stylesheet(self: SubredditUploader) -> bool:
        """checks if any sass files have been changed"""
        ending: str = "scss"
        head_commit: Dict[str, Any] = self.webhook["head_commit"]
        return any(
            path.splitext(file)[1] == ending
            for file in (head_commit["modified"] + head_commit["added"])
        )

    def upload_stylesheet(self: SubredditUploader, test: bool = False) -> bool:
        """compiles and uploads stylesheet"""
        style: str = ""
        try:
            style = sass.compile(
                filename=(self.path + "index.scss"), output_style="compressed")
        except sass.CompileError as sass_error:
            print(sass_error)
            return False

        try:
            subreddit = self.get_subreddit_test(test)
            subreddit.stylesheet.update(
                style, reason=self.upload_reason())
        except praw.exceptions.APIException as reddit_error:
            print(reddit_error)
            return False

        return True
