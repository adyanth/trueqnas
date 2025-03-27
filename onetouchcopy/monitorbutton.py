import evdev
from datetime import datetime
from .usbled import set, blink, trigger_disk_act
from .disk import disk

DEVICE_NAME = "qnap8528"
device, *_ = filter(lambda d: d.name == DEVICE_NAME, map(evdev.InputDevice, evdev.list_devices()))

def task_eject():
    # Task Eject
    print("Ejecting")
    try:
        disk().umount(force=True)
    except Exception as e:
        print(e)
    blink(3)

def task_start():
    print("Mounting and copying")
    blink(2)
    trigger_disk_act()
    # Task mount + copy
    with disk() as d:
        d.copy_to("/data/")
    set(False)

def run():
    LAST_DOWN_TIME = None
    print("Waiting for first event")
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            match key_event.keystate:
                case key_event.key_down:
                    LAST_DOWN_TIME = datetime.now()
                case key_event.key_up if LAST_DOWN_TIME is not None:
                    time_held = datetime.now() - LAST_DOWN_TIME
                    LAST_DOWN_TIME = None
                    if time_held.seconds >= 3:
                        task_eject()
                    else:
                        task_start()
            print("Waiting for next event")
