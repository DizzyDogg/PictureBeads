#!/bin/env python3

from collections import defaultdict

from PIL import Image

from colors import Colors

TILE_HEIGHT = TILE_WIDTH = 60
OUTPUT_SIZE = (40, 50)
COLORS_FILENAME = "data/bead_colors_perler_standard.json"

# Generate a palette from available colors
COLORS = Colors(COLORS_FILENAME)
PALETTE_IMAGE = COLORS.get_palette()


def adjust_channels(image, red=1.1, green=1.1, blue=1.1):
    return image.convert(mode="RGB").convert(
        mode="RGB",
        matrix=(red,   0,     0,     0,
                0,     green, 0,     0,
                0,     0,     blue,  0)
        )


def dither(image):
    return image.quantize(palette=PALETTE_IMAGE, method=0)


def resize(image, output_size=OUTPUT_SIZE):
    return image.resize(output_size, Image.LANCZOS)


def flip(image):
    from PIL.ImageOps import mirror

    return mirror(image)


def generate_template(image, flip=True):
    out_image = Image.new(
        "RGB",
        # Output size
        tuple(l * r for l, r in zip(OUTPUT_SIZE, COLORS.image_size)),
    )
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            color_name = COLORS.get_color_name(pixel)
            out_image.paste(
                COLORS.color_lookup[color_name]["image"],
                (x * TILE_WIDTH, y * TILE_HEIGHT)
            )
    return out_image


def count_beads(image):
    width, height = image.size
    color_counts = defaultdict(int)
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            color_name = COLORS.get_color_name(pixel)
            color_counts[color_name] += 1
    return color_counts


def generate_pixelart(image, red=1.0, green=1.0, blue=1.0):
    return dither(adjust_channels(resize(image), red, green, blue))


if __name__ == "__main__":
    in_image = Image.open("cropped.png")

    pixelart = generate_pixelart(in_image)

    print(count_beads(pixelart))
    generate_template(pixelart, flip=True).save("test.png", "PNG")
