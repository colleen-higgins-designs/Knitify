import requests

def get_color_link(colors):
  # get p_id
  landing_page = requests.get('https://halcyonyarn.com/yarn-colors/pick-yarns-by-color.php').text
  p_id_start_idx = landing_page.find('p_id') + 5
  p_id_end_idx = landing_page.find('#', p_id_start_idx)
  p_id = landing_page[p_id_start_idx:p_id_end_idx]



  data = {
    'image': '',
    'color0': '#gggggg',
    'color1': '#gggggg',
    'color2': '#gggggg',
    'color3': '#gggggg',
    'color4': '#gggggg',
    'number_results': 10,
  }

  for idx, (hex_value, name) in enumerate(colors.items()):
    data[f'color{idx}'] = hex_value

  # post to update colors
  requests.post(f'https://halcyonyarn.com/yarn-colors/pick-yarns-by-color.php?p_id={p_id}#yarnMatches', data=data)

  return f'https://halcyonyarn.com/yarn-colors/pick-yarns-by-color.php?p_id={p_id}#yarnMatches'
