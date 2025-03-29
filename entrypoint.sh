#!/bin/bash

(
    cd /app/qnap8528/src
    make
    rmmod qnap8528.ko || true
    insmod qnap8528.ko skip_hw_check=true
)
cd /app
python3 -u main.py 2> app.err | tee app.log
