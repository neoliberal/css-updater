"""holds information associated with Config File"""
from typing import Dict, Any, Tuple, Optional


# pylint: disable=R0903
class ConfigHandler(object):
    """see above"""

    def __init__(self: ConfigHandler, data: str) -> None:
        import json
        parsed: Dict[str, Any] = json.loads(data)["css_updater"]
        self.main: str = parsed["main"]
        self.assets: str = parsed["assets"]
        reddit: Dict[str, str] = parsed["reddit"]
        self.subreddits: Tuple[str, Optional[str]] = (reddit["main"], reddit["testing"])
        style: Dict[str, Any] = parsed["style"]
        self.style_type: str = style["type"]
        self.style_options: Dict[str, str] = style["options"]
