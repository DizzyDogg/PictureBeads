#!/bin/env python3

from PIL import Image
import numpy


layers = Image.open("Replacement_map.gif")
in_image = Image.open("cropped.png")

layers_array = numpy.asarray(layers)
in_array = numpy.asarray(in_image)

print(in_array)

print(len(in_array))
print(in_array[0])
print(len(in_array[0]))

out_array = in_array
out_image = Image.fromarray(out_array, "RGB")

out_image.save('test.png', 'PNG')
