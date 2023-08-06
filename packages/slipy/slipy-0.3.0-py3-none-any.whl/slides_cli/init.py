import pathlib

import slipy.new


def add_parser(subparsers):
    init_p = subparsers.add_parser("init", help=help["."])
    init_p.set_defaults(func=init)


def init(args):
    slipy.new.init(pathlib.Path(".").absolute())


help = {".": """Initialize project, populate assets"""}
