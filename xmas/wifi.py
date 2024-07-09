import network
import time
import ntptime

def connect(ssid, pwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #wlan.config(pm = 0xa11140) # no wifi sleep
    wlan.connect(ssid, pwd)

    # Wait for connect or fail
    ms = 10000
    period = 250
    while ms > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        ms -= period
        time.sleep_ms(period)
    
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')

    ntptime.settime()

    ip=wlan.ifconfig()[0]
    return (wlan,ip)
