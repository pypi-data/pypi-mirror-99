#!/usr/bin/env python3

import argparse
import subprocess
from io import BytesIO
from base64 import b64decode

from PIL import Image
import pyperclip


def from_image_data_url(folder, name):
    imagestr = pyperclip.paste()

    im = Image.open(BytesIO(b64decode(imagestr.split(",")[1])))
    im.save(folder / f"{name}.png")


def from_png(folder, name):
    result = subprocess.run(
        f"xclip -selection clipboard -t image/png -o".split(), stdout=subprocess.PIPE
    )
    with open(folder / f"{name}.png", "wb") as fd:
        fd.write(result.stdout)
