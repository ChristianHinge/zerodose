"""Utility functions."""
import os

import requests

from zerodose.paths import folder_with_parameter_files


def get_model_fname():
    """Returns the path to the parameter file for the given fold."""
    return os.path.join(folder_with_parameter_files, "model_1.pt")


def maybe_download_parameters(force_overwrite=False):
    """Downloads the parameters for some fold if it is not present yet.

    :param fold:
    :param force_overwrite: if True the old parameter file will be\
          deleted (if present) prior to download
    :return:
    """
    if not os.path.isdir(folder_with_parameter_files):
        maybe_mkdir_p(folder_with_parameter_files)

    out_filename = get_model_fname()

    if force_overwrite and os.path.isfile(out_filename):
        os.remove(out_filename)

    if not os.path.isfile(out_filename):
        url = "http://sandbox.zenodo.org/record/1165160/files/gen2.pt?download=1"
        print("Downloading", url, "...")
        data = requests.get(url)

        with open(out_filename, "wb") as f:
            f.write(data)


def maybe_mkdir_p(directory):
    """Creates a directory if it does not exist yet."""
    splits = directory.split("/")[1:]
    for i in range(0, len(splits)):
        if not os.path.isdir(os.path.join("/", *splits[: i + 1])):
            os.mkdir(os.path.join("/", *splits[: i + 1]))
