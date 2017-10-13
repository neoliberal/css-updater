"""updates subreddit css with compiled sass"""
import time

import sass
import praw


def css() -> str:
    """compiles sass and returns css"""
    return sass.compile(filename="index.scss", output_style="compressed")


def uid() -> str:
    """return date and time"""
    return "Subreddit upload on {}".format(time.strftime("%c"))

def update() -> None:
    """main function"""
    reddit: praw.Reddit = praw.Reddit()
    reddit.subreddit("neoliberal").stylesheet.update(css(), reason=uid())
    return
