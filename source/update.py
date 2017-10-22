"""updates subreddit css with compiled sass"""
import os
import time
from typing import List, Dict, Any, Tuple

import praw
import sass

WebhookResponse = Dict[str, Any] # pylint: disable=C0103


def css() -> str:
    """compiles sass and returns css"""
    return sass.compile(filename="index.scss", output_style="compressed")


def uid() -> str:
    """return date and time"""
    return "Subreddit upload on {}".format(time.strftime("%c"))


def changed_assets(data: WebhookResponse) -> Tuple[List[str], List[str]]:
    """identifies changed files to upload by checking if any changed files are images"""
    endings: List[str] = ["png", "jpg"]

    head_commit: Dict[str, Any] = data["head_commit"]

    uploading_files: List[str] = [
        file for file in (head_commit["modified"] + head_commit["added"])
        for ending in endings
        if os.path.splitext(file)[1] == ending
        ]
    removed_files: List[str] = [
        file for file in head_commit["removed"]
        for ending in endings
        if os.path.splitext(file)[1] == ending
    ]
    return (uploading_files, removed_files)

def update(data: WebhookResponse) -> None:
    """main function"""
    reddit: praw.Reddit = praw.Reddit()
    reddit.subreddit("neoliberal").stylesheet.update(css(), reason=uid())
    return
