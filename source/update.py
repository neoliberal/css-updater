"""updates subreddit css with compiled sass"""
from os import path
import time
from typing import List, Dict, Any, Tuple

import praw
import sass

# leave my typedefs alone, pylint: disable=C0103
WebhookResponse = Dict[str, Any]


def css() -> str:
    """compiles sass and returns css"""
    return sass.compile(filename="index.scss", output_style="compressed")


def uid() -> str:
    """return date and time"""
    return "Subreddit upload on {}".format(time.strftime("%c"))


def changed_assets(data: WebhookResponse) -> Tuple[List[str], List[str]]:
    """
    identifies changed assets to upload or remove by checking if any changed files are images
    returns a tuple containing modified / new files and removed files
    """
    endings: List[str] = ["png", "jpg"]

    head_commit: Dict[str, Any] = data["head_commit"]

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

def changed_spreedsheet(data: WebhookResponse) -> bool:
    """checks if any sass files have been changed"""
    ending: str = "scss"
    head_commit: Dict[str, Any] = data["head_commit"]
    return any(
        path.splitext(file)[1] == ending
        for file in (head_commit["modified"] + head_commit["added"])
    )


def update(data: WebhookResponse) -> None:
    """main function"""
    reddit: praw.Reddit = praw.Reddit()
    reddit.subreddit("neoliberal").stylesheet.update(css(), reason=uid())
    return
