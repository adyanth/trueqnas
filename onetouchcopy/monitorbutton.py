import evdev
from datetime import datetime
from multiprocessing import Process
from os import getenv
from .usbled import set, blink, trigger_disk_act
from .disk import disk

DEVICE_NAME = "qnap8528"

copy_process: Process = None

LONG_PRESS_MILLIS = int(getenv("LONG_PRESS_MILLIS", "1500"))


def copy_data():
    trigger_disk_act(state=True)
    with disk() as d:
        d.copy_to("/data/")
    trigger_disk_act(state=False)
    set(False)


def task_eject():
    # Task Eject
    print("task_eject")
    if copy_process and copy_process.is_alive():
        copy_process.kill()
        set(False)
    try:
        disk().umount(force=True)
    except Exception as e:
        print(e)
    blink(3)


def task_start():
    global copy_process
    if copy_process:
        if copy_process.is_alive():
            print("Already active, doing nothing")
            return
        copy_process.close()
    print("task_start")
    blink(2)
    # Task mount + copy
    copy_process = Process(target=copy_data)
    copy_process.start()


def run():
    LAST_DOWN_TIME = None
    device = next(
        filter(
            lambda d: d.name == DEVICE_NAME,
            map(evdev.InputDevice, evdev.list_devices()),
        )
    )
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
                    if time_held.total_seconds() * 1000 >= LONG_PRESS_MILLIS:
                        task_eject()
                    else:
                        task_start()
            print("Waiting for next event")
