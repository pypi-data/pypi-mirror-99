import sys
import pathlib
import logging
import inspect

import toml

from slipy_assets import template_cfg, Template, Theme

from . import utils
from . import update


logger = logging.getLogger(__name__)


def dump_gitignore(project_dir, extras=None):
    gitignore = inspect.cleandoc(
        """
        build
        .presentation
        """
    )
    if extras is not None:
        gitignore += f"\n{extras}"

    with open(project_dir / ".gitignore", "w") as fd:
        fd.write(gitignore)


def new(name, framework, framework_rebuild):
    project_dir = pathlib.Path(name)
    project_dir.mkdir()

    utils.switch_framework(framework).init(project_dir, framework_rebuild)

    presentation_cfg = template_cfg.copy()
    presentation_cfg["title"] = name
    presentation_cfg[framework] = utils.switch_framework(framework).set_initial_cfg(
        name
    )

    utils.dump_cfg(presentation_cfg, project_dir)
    dump_gitignore(project_dir, extras=utils.switch_framework(framework).gitignore)


def init(folder):
    logger.info("Initializing project...")
    project_dir = utils.find_project_dir(folder)

    presentation_cfg = utils.load_cfg(project_dir)
    framework = presentation_cfg["framework"]

    utils.switch_framework(framework).init(project_dir)

    assets_dir = project_dir / utils.assets_dir
    assets_dir.mkdir(exist_ok=True)

    update.update(project_dir)
