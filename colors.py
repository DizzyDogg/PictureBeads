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

        self.generate_color_lookup(filename)
        self.validate_color_lookup()
        self.generate_palette()
        self.generate_reverse_lookup()

        self.add_images(dir)

    def generate_color_lookup(self, filename):
        with open(filename) as beads_file:
            raw_color_lookup = json.load(beads_file)

        self.color_lookup = {}
        for color_name, values in raw_color_lookup.items():
            self.color_lookup[color_name] = {
                "rgb": tuple(values[:3]),
                "hex": values[3],
            }

    def validate_color_lookup(self):
        """
        Ensure that the RGB and hex values match up for each color
        """
        error_count = 0
        for color_name, color_data in self.color_lookup.items():
            if bytes(color_data["rgb"]).hex() != color_data["hex"].lower():
                print(
                    f'Color data mismatch for {color_name}:'
                    f' {color_data["rgb"][0]}, {color_data["rgb"][1]},'
                    f' {color_data["rgb"][2]} vs {color_data["hex"]}'
                )
                print('Given RGB converts to {}'.format(
                    bytes(color_data["rgb"]).hex()
                ))
                error_count += 1

    def generate_reverse_lookup(self):
        self.reverse_lookup = {}
        for color_name, values in self.color_lookup.items():
            self.reverse_lookup[values["rgb"]] = color_name
            self.reverse_lookup[values["hex"]] = color_name
        palette = self.palette.getpalette()
        palette_rgb = list(zip(palette[0::3], palette[1::3], palette[2::3]))
        for index, rgb in enumerate(palette_rgb):
            self.reverse_lookup[index] = self.reverse_lookup[rgb]

    def add_images(self, dir):
        for color_name in self.color_lookup.keys():
            filename = color_name.replace(" ", "_") + ".png"
            path = os.path.sep.join([self.image_dir, filename])

            try:
                image = Image.open(path)
                if (image.width, image.height) != self.image_size:
                    print(f"Incorrect image size for {color_name}:"
                          f" {image.width}*{image.height}")
                self.color_lookup[color_name]["image"] = image

            except (FileNotFoundError, IOError):
                print(f"Error reading image file for: {color_name}")
                fallback_image = Image.new(
                    "RGB",
                    self.image_size,
                    "#" + self.color_lookup[color_name]["hex"])
                self.color_lookup[color_name]["image"] = fallback_image

    def generate_palette(self):
        """
        Returns 3*256 bytes, representing the R, G, and B
        channels for each of 256 colors in the palette.
        """
        palette = []

        for color_data in self.color_lookup.values():
            palette.extend(color_data["rgb"])

        palette.extend(palette[:3] * (256 - len(self.color_lookup)))

        self.palette = Image.new('P', (16, 16))
        self.palette.putpalette(palette)

    def get_palette(self):
        return self.palette

    def get_color_name(self, color):
        try:
            return self.reverse_lookup[color.upper()]
        except AttributeError:
            return self.reverse_lookup.get(color, "Black")


def main():
    beads = Colors("bead_colors_perler_standard.json")
    print(beads.color_lookup["Apricot"])
    beads.color_lookup["Apricot"]["image"].show()


if __name__ == '__main__':
    main()
