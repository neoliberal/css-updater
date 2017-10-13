"""updates subreddit css with compiled sass"""
import subprocess
import praw

def css() -> str:
    """compiles sass and returns css"""
    res: subprocess.CompletedProcess = subprocess.run(
        "sass index.scss --style compressed --quiet", stdout=subprocess.PIPE
        )
    return res.stdout

def update(reddit: praw.Reddit, style: str) -> None:
    """update subreddit stylesheet"""
    sub: praw.models.Subreddit = reddit.subreddit("neoliberal")
    sub.wiki("config/stylesheet").update(style)
    return

def main() -> None:
    """main function"""
    reddit: praw.Reddit = praw.Reddit()
    style: str = css()
    update(reddit, style)
    return

if __name__ == '__main__':
    main()
