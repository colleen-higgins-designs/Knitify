from PIL import Image
import operator
from collections import defaultdict
import re
from functools import reduce
import numpy as np
from clarifai.rest import ClarifaiApp

input_path = './input/cat.jpg'
output_path = './output/output.png'

# Instantiate a new Clarifai app by passing in your API key.
app = ClarifaiApp(api_key='94c998fac8e248558b9c2d670e8de2c0')

# Choose one of the public models.
model = app.models.get('color')

# Predict the contents of an image by passing in a URL.
response = model.predict_by_filename(input_path)
input_colors = response["outputs"][0]["data"]["colors"]
palette = []

for row in input_colors:
  hex_color = row['raw_hex'].lstrip('#')
  palette.append(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

while len(palette) < 256:
    palette.append((0, 0, 0))

flat_palette = reduce(lambda a, b: a+b, palette)
assert len(flat_palette) == 768

palette_img = Image.new('P', (1, 1), 0)
palette_img.putpalette(flat_palette)

multiplier = 8
img = Image.open(input_path)
input_size = img.size
pixelSize = 10
output_size = (int(round(input_size[0] / pixelSize)), int(round(input_size[1] / pixelSize)))
img = img.resize((output_size[0] * multiplier, output_size[1] * multiplier), Image.BICUBIC)
img = img.quantize(palette=palette_img) #reduce the palette

img = img.convert('RGB')

out = Image.new('RGB', output_size)

for x in range(output_size[0]):
    for y in range(output_size[1]):
        #sample at get average color in the corresponding square
        histogram = defaultdict(int)
        for x2 in range(x * multiplier, (x + 1) * multiplier):
            for y2 in range(y * multiplier, (y + 1) * multiplier):
                histogram[img.getpixel((x2,y2))] += 1
        color = max(histogram.items(), key=operator.itemgetter(1))[0]
        out.putpixel((x, y), color)

out.save(output_path)
