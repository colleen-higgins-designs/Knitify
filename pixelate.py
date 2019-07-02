from PIL import Image
import operator
from collections import defaultdict
import re
from functools import reduce
import numpy as np
from clarifai.rest import ClarifaiApp
from enum import Enum

# Instantiate a new Clarifai app by passing in your API key.
app = ClarifaiApp(api_key='94c998fac8e248558b9c2d670e8de2c0')
class YarnSizes(Enum):
  LACE = 8
  SUPER_FINE = 30 / 4
  FINE = 6
  LIGHT = 22 / 4
  MEDIUM = 18 / 4
  BULKY = 13 / 4
  SUPER_BULKY = 9 / 4
  JUMBO = 6 / 4

class NeedleSizes(Enum):
  LACE = '000 to 1'
  SUPER_FINE = '1 to 3'
  FINE = '3 to 5'
  LIGHT = '5 to 7'
  MEDIUM = '7 to 9'
  BULKY = '9 to 11'
  SUPER_BULKY = '11 to 17'
  JUMBO = '17 and larger'

def pixelate(input_path, yarn_type, width):

  # Choose one of the public models.
  model = app.models.get('color')

  # Predict the contents of an image by passing in a URL.
  response = model.predict_by_filename(input_path)
  input_colors = response["outputs"][0]["data"]["colors"]
  palette = []
  color_names = {}

  for row in input_colors:
    hex_color = row['raw_hex'].lstrip('#')
    color_names[hex_color] = row['w3c']['name']
    palette.append(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

  while len(palette) < 256:
      palette.append(palette[0])

  flat_palette = reduce(lambda a, b: a+b, palette)
  assert len(flat_palette) == 768

  palette_img = Image.new('P', (1, 1), 0)
  palette_img.putpalette(flat_palette)

  img = Image.open(input_path)
  input_size = img.size

  output_width = int(round(YarnSizes[yarn_type].value * int(width)))
  output_size = (output_width, int(round(input_size[1] * output_width / input_size[0])))

  multiplier = 8
  img = img.resize((output_size[0] * multiplier, output_size[1] * multiplier), Image.BICUBIC)
  img = img.quantize(palette=palette_img) #reduce the palette

  img = img.convert('RGB')

  out = [[None] * output_size[0] for i in range(output_size[1])]
  used_color_names = {}

  for x in range(output_size[0]):
    for y in range(output_size[1]):
      #sample at get average color in the corresponding square
      histogram = defaultdict(int)
      for x2 in range(x * multiplier, (x + 1) * multiplier):
          for y2 in range(y * multiplier, (y + 1) * multiplier):
              histogram[img.getpixel((x2,y2))] += 1
      color = max(histogram.items(), key=operator.itemgetter(1))[0]
      out[y][x] = color
      hex_color = "".join(["%0.2X" % i for i in color]).lower()
      used_color_names[hex_color] = color_names[hex_color]


  return out, used_color_names

