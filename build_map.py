#!/bin/env python3

from PIL import Image

from colors import Colors


OUTPUT_SIZE = (40, 50)
COLORS_FILENAME = "bead_colors_perler_standard.json"

# Get image
in_image = Image.open("cropped.png")

# Resize image
scaled_image = in_image.resize((40, 50), Image.LANCZOS)

# Generate a palette from available colors
colors = Colors(COLORS_FILENAME)
palette_image = colors.get_palette()

# Adjust channels
R = 1.1
G = 1.1
B = 1.1
adjusted_image = scaled_image.convert(
    mode="RGB",
    matrix=(R, 0, 0, 0,
            0, G, 0, 0,
            0, 0, B, 0)
)

# Convert to bead colors
dithered_image = adjusted_image.convert(
    mode="P",
    dither=Image.FLOYDSTEINBERG,
    palette=palette_image
)

#dithered_image.show()

# Generate template
out_image = Image.new(
    "RGB",
    # Output size
    tuple(l * r for l, r in zip(OUTPUT_SIZE, colors.image_size)),
)
width, height = dithered_image.size
print(colors.color_lookup["Apricot"]["image"].size)
for y in range(height):
    for x in range(width):
        rgb = dithered_image.getpixel((x, y))
        color_name = colors.get_color_name(rgb)
        out_image.paste(
            colors.color_lookup[color_name]["image"],
            (x * 60, y * 60)
        )

# Display for debugging purposes
out_image.show()

# Write out to disk
out_image.save('test.png', 'PNG')
