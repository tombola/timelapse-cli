#!/usr/bin/env python

import os
import subprocess
from datetime import datetime
from time import sleep

os.getenv("HOME")
webcam = 'HD Pro Webcam C920'

filename_stub = 'timelapse'
destination = '{}/{}'.format(os.getenv("HOME"), filename_stub)
created_date = datetime.now().strftime("%Y%m%d_%H-%M")

count = 0
delay = 120 # seconds
limit = 14400 # seconds (4 hours)
max_count = int(limit / delay)
padding = len(str(max_count))

while count <= max_count:
    filename = '{}_{}'.format(
        filename_stub,
        created_date,
        str(count).zfill(padding) + '.jpg'
        )
    output_file = destination + '/' + filename
    subprocess.run(["imagesnap", "-d", webcam, output_file])
    sleep(1)
    subprocess.run(["clear"])
    print('{}/{}'.format(count, max_count))
    print('{} minutes recording time'.format(int((count*delay)/60)))
    print('{} second timelapse'.format(int(count/30)))
    count += 1
    sleep(delay - 1)
