FRONT_USB_SUBSTR = "0-usb-0:1"
MOUNT_PATH = "/mnt"
DEV_PATH = "/dev/disk/by-path/"
# /dev/disk/by-path/pci-0000:00:14.0-usb-0:1:1.0-scsi-0:0:0:0

from datetime import datetime
from os import listdir, mkdir
from os.path import join
from subprocess import check_call
import shutil
from shutil import copy, copytree
import traceback
import sys

# Disable folder permission mirroring
# https://stackoverflow.com/questions/1303413/python-shutil-copytree-ignore-permissions
shutil.copystat = lambda *a, **k: None

class disk:
    def __init__(self, mount_path: str = None):
        self.drive = join(
            DEV_PATH,
            next(
                filter(
                    lambda x: "part" in x,
                    filter(
                        lambda x: FRONT_USB_SUBSTR in x,
                        listdir(DEV_PATH),
                    ),
                ),
                next(
                    filter(
                        lambda x: FRONT_USB_SUBSTR in x,
                        listdir(DEV_PATH),
                    ),
                    "/dev/sr0"
                )
            ),
        )
        self.mounted = False
        if mount_path is None:
            self.mount_path = MOUNT_PATH
        else:
            self.mount_path = mount_path

    def mount(self):
        if self.mounted:
            print("Already mounted")
            return
        print(f"Mounting {self.drive} to {self.mount_path}")
        check_call(["/bin/mount", "-o", "ro", self.drive, self.mount_path])
        self.mounted = True
        print("Mounted")

    def __enter__(self):
        self.mount()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self.umount()

    def copy_to(self, dest: str):
        if not self.mounted:
            raise Exception("Not mounted, cannot copy")
        subpath = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = join(dest, subpath)
        print(f"Copying to {path}")
        try:
            if "VIDEO_TS" in listdir(self.mount_path):
                print("Making MKV from DVD")
                mkdir(path)
                check_call(["makemkvcon", "mkv", "dev:/dev/sr0", "all", path], stderr=sys.stderr, stdout=sys.stdout)
            else:
                copytree(self.mount_path, path, copy_function=copy)
        except Exception as e:
            from sys import stderr
            print(e, file=stderr)
        print("Copy complete")

    def umount(self, force: bool = False):
        if self.mounted or force:
            print("Unmounting")
            check_call(["/bin/umount", self.mount_path])
            self.mounted = False
            print("Unmounted")
            return
        print("Already unmounted and not forcing")

    def __del__(self):
        self.umount()
