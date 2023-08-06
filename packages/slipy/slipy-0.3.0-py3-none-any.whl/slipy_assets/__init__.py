import sys
import pathlib
import importlib
import shutil
import distutils.dir_util
import logging

import toml

from slipy import utils

# import framewokrs
from . import beamer
from . import reveal

logger = logging.getLogger(__name__)

here = pathlib.Path(__file__).parent

template_cfg = toml.load(here / "presentation.toml")


class Template:
    def __init__(self, name, framework):
        path = here / framework / "templates" / name

        self.template = path / "template.html"
        self.options = toml.load(path / "options.toml")
        self.examples = path / "examples"

        try:
            sys.path.insert(0, str(path.absolute()))
            self.update_build_context = importlib.import_module(
                "build"
            ).update_build_context
        except ModuleNotFoundError:
            self.update_build_context = lambda *args, **kwargs: None
        finally:
            sys.path.pop(0)

    def unpack(self, project_dir):
        assets_dir = project_dir / utils.assets_dir
        logger.debug(f"template -> [i]{assets_dir}[/]", extra={"markup": True})
        shutil.copy2(self.template, assets_dir)
        src_dir = assets_dir.parent.absolute() / "src"
        # unpack examples only if src does not exist or is empty
        if not src_dir.exists() or len(list(src_dir.iterdir())) == 0:
            logger.debug(
                f"unpacking template example -> [i]{src_dir}[/]", extra={"markup": True}
            )
            # since I don't want to copy the folder but only the content
            # I have to use distutils.dir_util instead of shutil.copytree
            distutils.dir_util.copy_tree(str(self.examples), str(src_dir))


class Slide:
    def __init__(self, metadata, content, force_format=""):
        self.metadata = metadata
        self.content = content
        self.force_format = force_format


class Theme:
    def __init__(self, name, framework):
        path = here / framework / "themes"
        self.name = name
        self.framework = framework

    def unpack(self, project_dir, dist_dir):
        theme_source = utils.switch_framework(self.framework).theme_path(
            self.name, project_dir, here
        )
        __import__("pdb").set_trace()
        try:
            theme_source.relative_to(project_dir)
            # the theme is built-in, no need to update
        except ValueError:
            assets_dir = project_dir / utils.assets_dir
            logger.debug(f"theme -> [i]{assets_dir}[/]", extra={"markup": True})
            shutil.copy2(theme_source, assets_dir)
