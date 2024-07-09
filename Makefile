files:=config.py leds.py main.py micropyserver.py webserver.py wifi.py public

default:
	@echo "Targets:\n put - copy all files to micropython device"

.venv:
	python3 -m venv .venv
	. .venv/bin/activate & pip install adafruit-ampy


put: .venv
	@if [ "$$AMPY_PORT" == "" ]; then echo "Error: AMPY_PORT is unset. try: ls /dev/tty.*"; exit 1; fi
	@. .venv/bin/activate & for f in ${files}; do echo "ampy put $$f"; ampy put $$f; done
