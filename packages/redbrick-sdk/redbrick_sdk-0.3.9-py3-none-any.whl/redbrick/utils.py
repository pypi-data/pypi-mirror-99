"""
Utility functions.
"""

from typing import List, Any
import requests
import numpy as np  # type: ignore
import cv2  # type: ignore
from redbrick.entity.taxonomy2 import Taxonomy2
import colorsys
import json
from distutils.version import StrictVersion
import subprocess
from redbrick.logging import print_warning
import redbrick
import os


def version_check() -> None:
    """Checks if current installed version of the SDK is up to date with latest pypi release."""
    # Getting latest version on pypi
    url = "https://pypi.org/pypi/{}/json".format("redbrick-sdk")
    data = requests.get(url).json()
    versions = list(data["releases"].keys())
    versions.sort(key=StrictVersion)
    latest_version = versions[-1]
    # Comparing with current installed version
    with open(
        os.path.join(os.path.dirname(redbrick.__file__), "VERSION"),
        "r",
        encoding="utf-8",
    ) as f:
        curr_version = f.read().strip()
    if curr_version != latest_version:
        warn = (
            "You are using version '{}' of the SDK. However, version '{}' is available!\n"
            + "Please update as soon as possible to get the latest features and bug fixes.\n"
            + "You can use 'python -m pip install --upgrade redbrick-sdk' to get the latest version."
        )
        print_warning(warn.format(curr_version, latest_version))


def clear_url(url: str) -> str:
    """Clears special characters from string"""
    url = url.replace("&", "AND").replace("/", "SLASH").replace("?", "QUESTION")
    return url


def generate_colors(num_colors: int) -> List[Any]:
    """Generates N different colors"""
    colors = []
    c = 1
    for i in np.arange(0.0, 360.0, 360.0 / num_colors):
        hue = i / 360.0
        lightness = (50 + (25 * (c % 2))) / 100.0
        saturation = (90 + (10 * (c % 2))) / 100.0
        # lightness = (50 + np.random.rand() * 10)/100.
        # saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
        c += 1
    return colors


def url_to_image(url: str) -> np.ndarray:
    """Get image data from url."""
    # Download the image, convert it to a NumPy array, and then read
    # it into OpenCV format

    resp = None

    try:
        resp = requests.get(url, stream=True)
        resp.raw.decode_content = True

        # check for errors
        if not resp.status_code == 200:
            raise Exception("Not able to access data at %s url" % (url))
    except Exception as err:
        raise Exception(
            "%s. Not able to access data at %s url" % (str(err), url)
        ) from err

    image = np.asarray(bytearray(resp.raw.read()), dtype="uint8")
    # pylint: disable=no-member
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # cv2 returns a BGR image, need to convert to RGB
    # the copy operation makes the memory contiguous for tensorify-ing
    return np.flip(image, axis=2).copy()


def compare_taxonomy(category_path: List[List[str]], taxonomy: Taxonomy2) -> bool:
    """Check if the category_path is valid for taxonomy."""
    tax_obj = taxonomy.taxonomy["categories"]

    for idx, cat in enumerate(category_path[0]):
        # Iterate through the tax obj
        for elem in tax_obj:
            if cat == elem["name"]:
                tax_obj = elem["children"]

                # Make sure this is the last category in path, and last elem in tax tree
                if len(tax_obj) == 0 and idx == len(category_path[0]) - 1:
                    return True

    return False
