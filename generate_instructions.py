
def generate_instructions(pattern, colors):

  cast_on = f'Cast on {len(pattern[0])} stitches'
  instructions = [cast_on]

  for row in pattern[::-1]:
    row_instructions = []
    num_to_knit = 0
    last_color = row[len(row) - 1]
    for cell in row[::-1]:
      if cell == last_color:
        num_to_knit += 1
      else:
        hex_color = "".join(["%0.2X" % i for i in last_color]).lower()
        row_instructions.append(f'k{num_to_knit} in {colors[hex_color]}')
        last_color = cell
        num_to_knit = 1
    if (num_to_knit == len(row)):
      num_to_knit = ' to end'
    hex_color = "".join(["%0.2X" % i for i in last_color]).lower()
    row_instructions.append(f'k{num_to_knit} in {colors[hex_color]}')
    instructions.append(f'{", ".join(row_instructions)}.')

  return instructions
