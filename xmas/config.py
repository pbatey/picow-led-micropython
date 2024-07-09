import json
import re

config = {
  'colors': [(0,0,0)],
  'spread': 1,
  'space_between': 1,
  'crawl': 1,
  'fade': 1,
  'period_ms': 250,
  'random': 5,
}

def to_color_tuples(hex_colors):
  if isinstance(hex_colors, list):
    l = len(hex_colors)
    color_tuples = [(0,0,0)] * l
    for i in range(l):
      h = hex_colors[i]
      try:
        color_tuples[i] = tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
      except:
        pass # leave black
    return color_tuples

def to_hex_colors(color_tuples:tuple[int,int,int]):
  l = len(color_tuples)
  hex_colors = [''] * len(color_tuples)
  for i in range(l):
    hex_colors[i] = '#%02x%02x%02x' % color_tuples[i]
  return hex_colors

_fixers = {
  'colors': to_color_tuples,
  'spread': (1,50),
  'space_between': (0,50),
  'crawl': (-1,1),
  'fade': (0,1),
  'period_ms': (10, 5000),
  'random': (0, 100),
}

def _fix(cfg):
  """ adjust/convert values so they don't exceed limits """
  if cfg is None:
    return None
  for key, fixer in _fixers.items():
    # validator is min/max
    if isinstance(fixer, tuple):
      if isinstance(cfg.get(key), int):
        cfg[key] = min(max(cfg[key], fixer[0]), fixer[1])
      elif key in cfg:
        del cfg[key]
    # validator is convert function
    if callable(fixer):
      cfg[key] = fixer(cfg.get(key))
      if cfg[key] is None:
        del cfg[key]
  return cfg

def update(new_config):
  new_config = _fix(new_config)
  if new_config is None:
    return False
  for key, value in config.items():
    config[key] = new_config.get(key, value)
  return True

def load():
  try:
    with open("config.json") as f:
      update(json.load(f))
      return True
  except:
    return False

def write():
  cfg = config.copy()
  cfg['colors'] = to_hex_colors(cfg['colors'])
  try:
    with open("config.json", "w") as f:
      f.write(json.dumps(cfg))
  except:
    pass
  return cfg
