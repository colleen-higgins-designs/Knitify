from PIL import Image

input_path = './input/bridge.jpg'
output_path = './output/line_output.png'

palette = [(255, 255, 255)]

while len(palette) < 256:
    palette.append((0, 0, 0))

palette_img = Image.new('P', (1, 1), 0)
palette_img.putpalette(flat_palette)
