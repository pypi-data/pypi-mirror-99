"""Template globals."""

from pprint import pformat
from textwrap import dedent

from understory.web import tx
from understory.web.indie.micropub import discover_post_type

__all__ = ["pformat", "tx", "discover_post_type", "dedent"]
