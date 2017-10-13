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


def update(reddit: praw.Reddit, style: str) -> None:
    """update subreddit stylesheet"""
    reddit.subreddit("neoliberal").stylesheet.update(style, reason=uid())
    return


def main() -> None:
    """main function"""
    reddit: praw.Reddit = praw.Reddit()
    style: str = css()
    update(reddit, style)
    return


if __name__ == '__main__':
    main()
