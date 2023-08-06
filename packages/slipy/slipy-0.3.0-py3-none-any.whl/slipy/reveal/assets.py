from slipy_assets import Template, Theme


def update_template(name, project_dir):
    template = Template(name, "reveal")
    template.unpack(project_dir)

    return template.options


def update_theme(name, project_dir, dist_dir):
    theme = Theme(name, "reveal")

    theme.unpack(project_dir, dist_dir)
