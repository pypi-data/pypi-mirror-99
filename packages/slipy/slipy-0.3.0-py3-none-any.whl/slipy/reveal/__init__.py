import pathlib

from .. import utils
from . import assets
from . import get
from . import view


def set_initial_cfg(name):
    reveal_cfg = {}
    reveal_cfg["dist_dir"] = ".reveal_dist"
    reveal_cfg["plugins"] = ["math"]

    return reveal_cfg


gitignore = """
# reveal.js
.reveal_dist
"""


def init(project_dir, force_rebuild=False, force_download=False):
    force = force_rebuild or force_download
    if not (project_dir / ".reveal_dist").exists() or force:
        get.get_reveal(project_dir, force_rebuild)


dist_files = ".reveal_dist"
dev_files = [".presentation"]
theme_dir = str(pathlib.Path(dist_files) / "dist" / "theme")


def clean(folder):
    """
    Clean unneeded generated files
    """
    pass


def theme_path(name, project_dir, slipy_assets):
    theme_dir = slipy_assets / "reveal" / "themes"
    if (theme_dir / (name + ".css")).exists():
        return theme_dir / (name + ".css")
    else:
        return project_dir / dist_files / "dist" / "theme" / (name + ".css")
