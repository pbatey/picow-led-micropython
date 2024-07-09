import neopixel
import machine
import _thread
import time
import random

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 127, 0)
yellow = (255, 255, 0)
chartreuse = (127, 255, 0)
green = (0, 255, 0)
springGreen = (0, 255, 127)
cyan = (0, 255, 255)
azure = (0, 127, 255)
blue = (0, 0, 255)
violet = (127, 0, 255)
magenta = (255, 0, 255)
rose = (255, 0, 127)

rainbow = [red, orange, yellow, chartreuse, green, springGreen, cyan, azure, blue, violet, magenta, rose]
xmas = [red, white, green]
xmas_alt = [red, blue, orange, green, yellow]

_default_nleds = 1200
_default_pin = 0

class Leds(object):

  def __init__(self, config={}):
    if isinstance(config, list):
      self.config = {'colors': config}
    if isinstance(config, tuple):
      self.config = {'colors': [config]}
    if isinstance(config, dict):
      self.config = config
    self.exit = False
    self.leds = None
    self.pin = None
    self._alloc()
    self.avgtick = 0
    self._nticks = 0

  def _alloc(self):
    if not self._need_realloc():
      return
    self.pin = self.config.get('pin', _default_pin)
    nleds = self.config.get('nleds', _default_nleds)
    self.leds = neopixel.NeoPixel(machine.Pin(self.pin), nleds)
    self.fill(show=True)

  def _need_realloc(self):
    if self.leds is None:
      return True
    pin = self.config.get('pin', _default_pin)
    if pin != self.pin:
      return True
    nleds = self.config.get('nleds', _default_nleds)
    if nleds != self.leds.n:
      return True
    return False

  def fill(self, colors=None, show=False):
    fill(self, colors, show)
  def fillr(self, r=None, colors=None, show=False):
    fillr(self, r, colors, show)
  def crawl(self, d=None, show=False):
    crawl(self, d, show)
  def fade(self, f=None, show=False):
    fade(self, f, show)
  def show(self):
    self.leds.write()

  def clear(self):
    clear(self, show=False)

  def tick(self):
    self.crawl(self.config.get('crawl',0))
    self.fade(self.config.get('fade',0))
    self.fillr(self.config.get('random',0), self.config.get('colors'))
    self.leds.write()

  def _update_avgtick(self, ms):
    if ms > 0:
      self.avgtick = (self.avgtick * self._nticks + ms)/(self._nticks + 1)
      self._nticks += 1
    if self._nticks > 10:
      self._nticks = 0

  def loop(self):
    while True:
      if self.exit:
        break
      start_ms = time.ticks_ms()
      self.tick()
      elapsed_ms = time.ticks_ms() - start_ms
      self._update_avgtick(elapsed_ms)
      period_ms = self.config.get('period_ms', 250)
      next_ms = int(period_ms - elapsed_ms)
      if next_ms <= 0:
        next_ms = period_ms
      time.sleep_ms(next_ms)

  def start(self, inthread=True):
    self.exit = False
    if inthread:
      _thread.start_new_thread(self.loop, ())
    else:
      self.loop()

  def stop(self):
    self.exit = True

if __name__ == "__main__":
  config = {
    'colors': xmas,
    'spread': 1,
    'space_between': 0,
    'crawl': 1,
    'fade': 1,
    'period_ms': 250,
    'random': 5,
  }
  l = Leds(config)
  l.start(config, inthread=False)


@micropython.native
def fade(l:Leds, f=None, show=True):
  f = f if f is not None else l.config.get('fade', 50)
  # fade (0,1) 1=on
  #f = min(max(f,0),1)
  if f == 0:
    return
  for i in range(l.leds.n * l.leds.bpp):
    l.leds.buf[i] >>= 1
  l.filled = False
  if show:
    l.leds.write()

@micropython.native
def crawl(l:Leds, d=0, show=True):
  if d == 0:
    return
  # crawl (0, -1, 1) -1=left, 1=right
  #d = min(max(d,-1),1)
  shift = -d * l.leds.bpp
  if shift != 0:
    l.leds.buf[:] = l.leds.buf[shift:] + l.leds.buf[:shift]
  if show:
    l.leds.write()

@micropython.native
def fillr(l:Leds, r=0, colors=None, show=True):
  if r == 0 or colors is None:
    return
  # fill random (0..100)
  #r = min(max(r,0),100)
  rleds = range(l.leds.n)
  rcolors = range(len(colors))
  for x in range(int(l.leds.n * r/100)):
    i = random.choice(rleds)
    j = random.choice(rcolors)
    l.leds[i] = colors[j]
  l.filled = False
  if show:
    l.leds.write()

@micropython.native
def fill(l:Leds, colors=None, show=True):
  if colors is None:
    return
  if isinstance(colors, tuple):
    l.leds.fill(colors) # single color
  elif isinstance(colors, list):
    ncolors = len(colors)
    for i in range(l.leds.n):
      l.leds[i] = colors[i % ncolors]
  l.filled = True
  if show:
    l.leds.write()

def clear(l:Leds, show=True):
  l.leds.fill(black)
  if show:
    l.leds.write()
