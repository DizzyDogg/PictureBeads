#!/usr/bin/env python3


import json
import os

from PIL import Image


IMAGE_SIZE = (60, 60)
IMAGE_DIR = "./color_images/bitmap"


class Colors:

    def __init__(self, filename, image_size=IMAGE_SIZE, image_dir=IMAGE_DIR):
        self.filename = filename
        self.image_size = image_size
        self.image_dir = image_dir

        with open(filename) as beads_file:
            raw_color_dictionary = json.load(beads_file)

        self.color_dictionary = {}
        for color_name, values in raw_color_dictionary.items():
            self.color_dictionary[color_name] = {
                "rgb": tuple(values[:3]),
                "hex": values[3],
            }

        self.validate_color_dictionary()

        self.add_images(dir)

    def validate_color_dictionary(self):
        """
        Ensure that the RGB and hex values match up for each color
        """
        error_count = 0
        for color_name, color_data in self.color_dictionary.items():
            if bytes(color_data["rgb"]).hex() != color_data["hex"].lower():
                print('Color data mismatch for {}: {}, {}, {} vs {}'.format(
                    color_name, *color_data["rgb"], color_data["hex"]))
                print('Given RGB converts to {}'.format(
                    bytes(color_data["rgb"]).hex()))
                error_count += 1
        #if error_count:
            #import sys
            #sys.exit(error_count)

    def add_images(self, dir):
        for color_name in self.color_dictionary.keys():
            filename = "{}.png".format(color_name)
            path = os.path.sep.join([self.image_dir, filename])

            try:
                image = Image.open(path)
                if (image.width, image.height) != self.image_size:
                    print(f"Incorrect image size for {color_name}:"
                          " {image_width}*{image_height}")
                self.color_dictionary[color_name]["image"] = image

            except (FileNotFoundError, IOError):
                print(f"Error reading image file for: {color_name}")
                fallback_image = Image.new(
                    "RGB",
                    self.image_size,
                    "#" + self.color_dictionary[color_name]["hex"])
                self.color_dictionary[color_name]["image"] = fallback_image

    def get_palette(self):
        """
        Returns 3*256 bytes, representing the R, G, and B
        channels for each of 256 colors in the palette.
        """
        palette = []

        for color_data in self.color_dictionary.values():
            palette.extend(color_data[:3])

        palette.extend(palette[:3] * (256 - len(self.color_dictionary)))

        return bytes(palette)


def main():
    beads = Colors("bead_colors_perler_standard.json")
    print(beads.color_dictionary["Apricot"])
    beads.color_dictionary["Apricot"]["image"].show()


if __name__ == '__main__':
    main()
