from pathlib import Path
import time

QNAP_USB_LED = Path("/sys/class/leds/qnap8528::usb/")

def set(state: bool):
    with open(QNAP_USB_LED / "brightness", "w") as f:
        f.write("1" if state else "0")

def blink(count: int=1, delays: float=0.5):
    for _ in range(count):
        set(state=True)
        time.sleep(delays)
        set(state=False)
        time.sleep(delays)

def trigger_disk_act(state: bool):
    with open(QNAP_USB_LED / "trigger", "w") as f:
        f.write("usb-host" if state else "none")
