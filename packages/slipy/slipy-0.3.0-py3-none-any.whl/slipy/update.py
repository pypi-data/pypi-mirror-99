import pathlib
import logging

from . import utils

logger = logging.getLogger(__name__)


def update(folder):
    project_dir = utils.find_project_dir(folder)

    presentation_cfg = utils.load_cfg(project_dir)
    template_options = update_template(project_dir, presentation_cfg)
    update_theme(project_dir, presentation_cfg)

    presentation_cfg = update_template_options(presentation_cfg, template_options)

    utils.dump_cfg(presentation_cfg, project_dir)


def update_template(project_dir, presentation_cfg):
    framework = presentation_cfg["framework"]
    name = presentation_cfg["template"]["name"]

    logger.info(f"Update [red]Template[/] [i magenta]{name}[/]", extra={"markup": True})

    return utils.switch_framework(framework).assets.update_template(name, project_dir)


def update_template_options(presentation_cfg, template_options):
    presentation_cfg = presentation_cfg.copy()

    print_header = True
    for k, opt in template_options.items():
        if k in presentation_cfg["template"] and opt != presentation_cfg["template"][k]:
            if print_header:
                print("Updating 'template' section in 'presentation.toml'")
                print("--------------------------------------------------")

            print_header = False
            print(f"> {k} = {presentation_cfg['template'][k]}")
            ans = input(f"Do you want to update with '{opt}'? [y/N]")
            if ans.lower() in ["y", "yes"]:
                presentation_cfg["template"][k] = opt
                print("✓ updated")
            else:
                print("✗ old one kept")
        else:
            presentation_cfg["template"][k] = opt

    return presentation_cfg


def update_theme(project_dir, presentation_cfg):
    framework = presentation_cfg["framework"]
    name = presentation_cfg["theme"]["name"]
    dist_dir = project_dir / presentation_cfg[framework]["dist_dir"]

    logger.info(f"Update [red]Theme[/] [i magenta]{name}[/]", extra={"markup": True})

    utils.switch_framework(framework).assets.update_theme(name, project_dir, dist_dir)
