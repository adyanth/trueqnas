#!/bin/env python3

import onetouchcopy
from time import sleep

if __name__ == "__main__":
    print("Starting...")
    while True:
        try:
            onetouchcopy.run()
        except Exception as e:
            print(e)
            sleep(1)
