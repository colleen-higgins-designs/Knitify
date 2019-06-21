from PIL import Image, ImageFilter

input_path = './input/cat.jpg'
output_path = './output/edgedetect.png'

img = Image.open(input_path)

pixelSize = 10
output_size = (int(round(input_size[0] / pixelSize)), int(round(input_size[1] / pixelSize)))
img = img.resize((input_size[0], input_size[1]), Image.BICUBIC)

pixel = img.load()


for i in range(0, output_size[0]-pixelSize, pixelSize):
  for j in range(0, output_size[1]-pixelSize, pixelSize):
    for r in range(pixelSize):
      pixel[i+r, j] = (0, 0, 0)
      pixel[i, j+r] = (0, 0, 0)

img.save(output_path)


# from PIL import Image

# backgroundColor = (0,)*3
# pixelSize = 9

# image = Image.open('input.png')
# image = image.resize((image.size[0]/pixelSize, image.size[1]/pixelSize), Image.NEAREST)
# image = image.resize((image.size[0]*pixelSize, image.size[1]*pixelSize), Image.NEAREST)
# pixel = image.load()

# for i in range(0,image.size[0],pixelSize):
#   for j in range(0,image.size[1],pixelSize):
#     for r in range(pixelSize):
#       pixel[i+r,j] = backgroundColor
#       pixel[i,j+r] = backgroundColor

# image.save('output.png')
