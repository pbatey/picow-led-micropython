
## Install micropython on to the Pico

1. First connect the pico as a usb by holding down the BOOTSEL while attaching to your Mac.

2. Get the micropython distro

   ```
   curl -O https://micropython.org/resources/firmware/RPI_PICO_W-20240602-v1.23.0.uf2
   ```

   Note: visit https://micropython.org/download/RPI_PICO_W for the latest release.

3. **Mount the _Pico W_ to the Mac:** With the _Pico W_'s power off,
   press and hold the **BOOTSEL** button while connecting the
   _Pico W_ to your Mac. It'll take around 3 seconds for it to
   show up on the desktop.

4. Copy the MicroPython uf2 file to the device. It'll reset by 
   itself. If shown, you can safely ingore the "Disk Not Ejected Properly"
   warning.

   ```
   cp RPI_PICO-20231005-v1.21.0.uf2 /Volumes/RPI-RP2
   ```

## Serial Port connection for Python REPL running on the Pico

You can watch the output of your program by connecting to the terminal

```
brew install tio
tio /dev//tty.usbmodem31343101
```

## Copy the python app to the Pico

1. initiate a local python env

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. install ampy

   ```
   pip3 install adafruit-ampy
   export AMPY_PORT=/dev//tty.usbmodem31343101
   ampy put main.py
   ```

3. restart the pi

   ```
   tio /dev/ttyACM0
   machine.reset()
   ```

## Troubleshooting

### Factory reset

If you get into a situation where you are unable to connect to the micropython terminal using tio or
cannot type anything into the terminal due to multiple threads causing problems...

Try resetting the _Pico W_ to factory settings by installing **flash_nuke.uf2** to remove any python files, such as **main.py**.

1. Download the **flash_nuk.uf2** image

```
curl -O https://github.com/dwelch67/raspberrypi-pico/raw/main/flash_nuke.uf2
```

2. **Mount the _Pico W_ to the Mac:** With the _Pico W_'s power off,
   press and hold the **BOOTSEL** button while connecting the
   _Pico W_ to your Mac. It'll take around 3 seconds for it to
   show up on the desktop.

3. Copy the _flash_nuke.uf2_ file to the device. It'll reset by
   itself. If shown, you can safely ingore the "Disk Not Ejected Properly"
   warning.

   ```
   cp flash_nuke.uf2 /Volumes/RPI-RP2
   ```

