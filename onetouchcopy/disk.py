FRONT_USB_SUBSTR = "0-usb-0:1"
MOUNT_PATH = "/mnt"
DEV_PATH = "/dev/disk/by-path/"
# /dev/disk/by-path/pci-0000:00:14.0-usb-0:1:1.0-scsi-0:0:0:0

from datetime import datetime
from os import listdir
from os.path import join
from subprocess import check_call
from shutil import copy, copytree


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
                )
            ),
        )
        self.mounted = False
        if mount_path is None:
            self.mount_path = MOUNT_PATH
        else:
            self.mount_path = mount_path

    def mount(self):
        if not self.mounted:
            check_call(["/bin/mount", self.drive, self.mount_path])
            self.mounted = True

    def __enter__(self):
        self.mount()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            import traceback
            traceback.print_exception(exc_type, exc_value, tb)
        self.umount()

    def copy_to(self, dest: str):
        if not self.mounted:
            raise Exception("Not mounted, cannot copy")
        subpath = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = join(dest, subpath)
        print(f"Copying to {path}")
        copytree(self.mount_path, path, copy_function=copy)

    def umount(self, force: bool = False):
        if self.mounted or force:
            check_call(["/bin/umount", self.mount_path])
            self.mounted = False

    def __del__(self):
        self.umount()
