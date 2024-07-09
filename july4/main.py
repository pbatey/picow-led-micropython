import wifi
import webserver
from leds import Leds
import config as cfg

cfg.load()
leds = Leds(cfg.config)
leds.start()

(wlan, ip) = wifi.connect('sunlight4','Inigo Montoya2013')
try:
  webserver.start(ip=ip, load_config=False, leds=leds)
except KeyboardInterrupt:
  pass
finally:
  leds.stop()
  wlan.disconnect()

