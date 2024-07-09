from micropyserver import MicroPyServer, static_files, Request, Response
import config

version = {
  'app': 'pico-led-micropython',
  'version': '1.0.0',
}

def get_config(req:Request, res:Response):
  """ GET /api/v1/config """
  c = config.config.copy()
  c['colors'] = config.to_hex_colors(c['colors'])
  res.send(c)

def post_config(req:Request, res:Response):
  """ POST /api/v1/config """
  if config.update(req.json()):
    c = config.write()
    res.send(c)
  else:
    get_config(req, res)

def start(port=80, ip='localhost', load_config=True, leds=None):
  if load_config:
    config.load()
  server = MicroPyServer(ip=ip, port=port)
  server.add_route("/api/v1/version", lambda req,res: res.send(version))
  server.add_route("/api/v1/config", get_config)
  server.add_route("/api/v1/config", post_config, method="POST")
  if leds is not None:
    server.add_route("/api/v1/metrics", lambda req,res: res.send({'avgtick_ms':leds.avgtick}))
  server.on_not_found(static_files(basedir='public'))
  try:
    server.start()
  except KeyboardInterrupt:
    pass
  finally:
    server.stop()

if __name__ == "__main__":
  start(3000)

