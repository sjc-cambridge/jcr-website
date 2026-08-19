import os

from dotenv import load_dotenv

"""
Resolves the private data directory: minutes, transparency, elections data,
exceptions.json and the johnians list all live here instead of in the git
tree, so uploads never dirty the working tree and can't be committed by
mistake. (Secret keys live in .env instead, see .env.example.)

Set PRIV_DIR in a .env file or the environment to point at it; defaults to
<repo>/private for local dev.
"""

load_dotenv()

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIV_DIR = os.path.abspath(
    os.environ.get("PRIV_DIR", os.path.join(_repo_root, "private"))
)

if not os.path.isdir(PRIV_DIR):
    raise RuntimeError(
        "Private data directory not found: {}\n"
        "Set PRIV_DIR in .env, or create ./private (see README).".format(PRIV_DIR)
    )
