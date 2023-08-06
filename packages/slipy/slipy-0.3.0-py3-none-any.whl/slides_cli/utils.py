import pathlib


def add_parser(subparsers):
    utils_p = subparsers.add_parser("utils", help=help["."])
    available_utils = utils_p.add_subparsers()
    clipng_p = available_utils.add_parser("clipng", help=help["clipng"]["."])
    clipng_p.add_argument("name", help=help["clipng"]["name"])
    clipng_p.add_argument(
        "-u", "--data-url", action="store_true", help=help["clipng"]["data-url"]
    )
    clipng_p.set_defaults(func=clipng)


def clipng(args):
    from slipy.utils import clipng

    if args.data_url:
        clipng.from_image_data_url(pathlib.Path(".").absolute(), args.name)
    else:
        clipng.from_png(pathlib.Path(".").absolute(), args.name)


help = {
    ".": """Command line utilities for writing presentations""",
    "clipng": {
        ".": """Dump picture from clipboard on file""",
        "name": """the name for the file to dump""",
        "data-url": """use clipboard content as Image Data-URL""",
    },
}
