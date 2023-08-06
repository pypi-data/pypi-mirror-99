"""
Code relating to camera metadata, such as generating or reading metadata files.
"""

import numpy as np
import json
from collections import namedtuple

from . import raw, analyse
from .general import return_with_filename

def _convert_exposure_time(exposure):
    """
    Convert an exposure time, in various formats, into a floating-point number.
    """
    if isinstance(exposure, (float, int)):
        # If the input is already a number, simply return it
        return exposure
    elif isinstance(exposure, str):
        # If the input is a string, e.g. from the command line
        if "/" in exposure:
            # If a fraction (e.g. '1/3', '2/5.1') is given, simply evaluate
            # it and return the result
            num, den = [float(x) for x in exposure.split("/")]
            return num/den

        elif "." in exposure:
            # If a decimal number (e.g. '2.5' or '0.002') is given, simply
            # convert it to a floating point number and return the result
            return float(exposure)

        else:
            # If a simple number is given (e.g. '2' or '100'), simply convert
            # it to a floating point number and return the result
            return float(exposure)
    else:
        # If the input is none of the above, try to cast it to a float somehow
        try:
            exposure_new = float(exposure)
        except TypeError:
            # Raise an error if the exposure could not be converted
            raise TypeError(f"Input exposure `{exposure}` is of type `{type(exposure)}` which cannot be converted to a number.")
        else:
            # If the exposure could be converted, return it
            return exposure_new


class Camera(object):
    """
    Class that represents a camera, providing some metadata used in common
    calibration/analysis tasks. Some class methods for common tasks are also
    included, such as generating a Bayer map.
    """
    # Properties a Camera can have
    Device = namedtuple("Device", ["manufacturer", "name"])
    Image = namedtuple("Image", ["shape", "raw_extension", "bias", "bayer_pattern", "bit_depth"])
    Settings = namedtuple("Settings", ["ISO_min", "ISO_max", "exposure_min", "exposure_max"])

    def __init__(self, device_properties, image_properties, settings):
        """
        Generate a Camera object based on input dictionaries containing the
        keys defined in Device, Image, and Settings
        """
        # Convert the input exposures to floating point numbers
        settings["exposure_min"] = _convert_exposure_time(settings["exposure_min"])
        settings["exposure_max"] = _convert_exposure_time(settings["exposure_max"])

        # Create named tuples based on the input dictionaries
        self.device = self.Device(**device_properties)
        self.image = self.Image(**image_properties)
        self.settings = self.Settings(**settings)

        # Generate/calculate commonly used values/properties
        self.bayer_map = self.generate_bayer_map()
        self.saturation = 2**self.image.bit_depth - 1

    def __repr__(self):
        """
        Output for `print(Camera)`, currently simply the name of the device
        """
        device_name = f"{self.device.manufacturer} {self.device.name}"
        return device_name

    def _as_dict(self):
        """
        Generate a dictionary containing the Camera metadata, similar to the
        inputs to __init__.
        """
        dictionary = {"device": self.device._asdict(),
                      "image": self.image._asdict(),
                      "settings": self.settings._asdict()}
        return dictionary

    def generate_bayer_map(self):
        """
        Generate a Bayer map, with the Bayer channel (RGBG2) for each pixel.

        To do:
            * Hide method (single underscore)
        """
        bayer_map = np.zeros(self.image.shape, dtype=int)
        bayer_map[0::2, 0::2] = self.image.bayer_pattern[0][0]
        bayer_map[0::2, 1::2] = self.image.bayer_pattern[0][1]
        bayer_map[1::2, 0::2] = self.image.bayer_pattern[1][0]
        bayer_map[1::2, 1::2] = self.image.bayer_pattern[1][1]
        return bayer_map

    def generate_bias_map(self):
        """
        Generate a Bayer-aware map of bias values from the camera metadata
        """
        bayer_map = self.generate_bayer_map()
        for j, bias_value in enumerate(self.image.bias):
            bayer_map[bayer_map == j] = bias_value
        return bayer_map

    def generate_ISO_range(self):
        """
        Generate an array with all ISO values possible for this camera.

        To do:
            * Hide method and use a property instead (like the bayer map)
        """
        return np.arange(self.settings.ISO_min, self.settings.ISO_max+1, 1)

    def write_to_file(self, path):
        """
        Write metadata to a file.
        """
        write_json(self._as_dict(), path)

    def demosaick(self, *data, **kwargs):
        """
        Demosaick data using this camera's Bayer pattern.
        """
        RGBG_data = raw.demosaick(self.bayer_map, *data, **kwargs)
        return RGBG_data

    def plot_gauss_maps(self, data, **kwargs):
        """
        Plot Gaussian maps using analyse.plot_gauss_maps.
        Uses this camera's Bayer pattern.
        """
        analyse.plot_gauss_maps(data, self.bayer_map, **kwargs)

    def plot_histogram_RGB(self, data, **kwargs):
        """
        Plot an RGB histogram maps using analyse.plot_gauss_maps.
        Uses this camera's Bayer pattern.
        """
        analyse.plot_histogram_RGB(data, self.bayer_map, **kwargs)

    @classmethod
    def read_from_file(cls, path):
        """
        Read metadata from a JSON file.
        """
        full_dictionary = load_json(path)
        device_properties, image_properties, settings = full_dictionary.values()
        return cls(device_properties, image_properties, settings)


def load_json(path):
    """
    Read a JSON file.
    """
    with open(path, "r") as file:
        try:
            # Load the JSON file
            dump = json.load(file)
        except json.JSONDecodeError:
            # If the JSON file could not be read, e.g. because it is empty, raise an error
            raise ValueError(f"Could not read JSON file `{path}`.")
    return dump


def write_json(data, save_to):
    """
    Write a JSON file containing `data` to a path `save_to`.
    """
    with open(save_to, "w") as file:
        json.dump(data, file)


def load_metadata(root, return_filename=False):
    """
    Read the metadata JSON located in the `root` folder.

    If `return_filename` is True, also return the exact filename used.
    """
    filename = root/"metadata.json"
    metadata = Camera.read_from_file(filename)
    return return_with_filename(metadata, filename, return_filename)
