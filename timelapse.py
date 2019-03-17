#!/usr/bin/env python3

import os
import re
import subprocess
from datetime import datetime, timedelta
from time import sleep
import argparse
from pytimeparse import parse


parser = argparse.ArgumentParser()
parser.add_argument('delay', nargs='?', default=30, help='Delay in seconds')
parser.add_argument('duration', nargs='?', default='00:30:00', help='Total recording duration, any format, no spaces')
parser.add_argument('--framerate', '-r', help='Delay in seconds', default=30)
parser.add_argument('--name', '-n', help='Destination filename for timelapse', default='timelapse')
parser.add_argument('--folder', '-f', help='Destination folder for timelapse', default=None)
parser.add_argument('--webcam', '-w', help='Webcam (see `imagesnap -l` for name)', default=None)
parser.add_argument('--date', '-d', help='Add the date', action='store_true', default=False)
parser.add_argument('--compile', '-c', help='Compile (with ffmpeg)', action='store_true', default=False)
parser.add_argument('--list', '-l', help='List available webcams', action='store_true', default=False)

args = parser.parse_args()

if not args.folder:
    created_date = datetime.now().strftime("%Y%m%d_%H-%M")
    default_folder = default = os.getcwd() + '/' + args.name + '_' + created_date
    args.folder = default_folder

# recording parameters
filename_stub = args.name
destination = args.folder
count = 0
delay = int(args.delay) # seconds
duration = int(parse(args.duration)) # seconds

# compile parameters
ffmpeg = args.compile
framerate = f'1/{int(args.framerate)}' # frames per seconds

# inferred parameters
max_count = int(duration/delay)
padding = len(str(max_count))


def express_duration(seconds):
    days = seconds//86400
    hours = (seconds - days*86400)//3600
    minutes = (seconds - days*86400 - hours*3600)//60
    seconds = seconds - days*86400 - hours*3600 - minutes*60
    result = f'{days}d, ' \
        f'{hours}hr, ' \
        f'{minutes}min, ' \
        f'{seconds}sec'
    return result

def get_webcam_list():
    webcam_list = subprocess.check_output("imagesnap -l;", stderr=subprocess.STDOUT, shell=True)
    return re.findall(r"\[(.*?)\]", str(webcam_list))[0::2]

def get_webcam(preferred='HD Pro Webcam C920'):
    webcams = get_webcam_list()
    return preferred if preferred in webcams else webcams[0]

def get_filepath(count, as_pattern=False):
    # import pudb; pudb.set_trace()
    filename = filename_stub
    if args.date:
        f'{filename}_{created_date}'
    if as_pattern:
        pattern = f'%{str(padding).zfill(2)}'
        filename += f'_{pattern}d.jpg'
    else:
        filename += f'_{str(count).zfill(padding)}.jpg'

    return f'{destination}/{filename}'

def check_destination():
    if not os.path.isdir(destination):
        try:
            os.mkdir(destination)
        except OSError:
            print("Destination folder %s couldn't be created" % destination)


if args.list:
    for webcam in get_webcam_list():
        print(webcam)
    quit()

webcam = args.webcam or get_webcam()

print(f'Capturing every {delay} seconds from {webcam}')
print(f'- total recording duration {express_duration(duration)}')
print(f'- saving output to {destination}')
if ffmpeg:
    print('- compiling images into video')

check_destination()

while count <= max_count:
    output = get_filepath(count)
    subprocess.run(["imagesnap", "-d", webcam, output])
    sleep(1)
    subprocess.run(["clear"])
    print(f'{count}/{max_count}')
    print(f'{int((count*delay)/60)} minutes recording time')
    print(f'{int(count/30)} second timelapse')
    count += 1
    sleep(delay - 1)

while not os.path.exists(get_filepath(max_count)):
    print('.')
    sleep(0.5)

if ffmpeg:
    filename_pattern = get_filepath(0, as_pattern=True)
    ffmpeg_command = [
        'ffmpeg',
        '-loglevel', 'panic',       # run silent
        '-f', 'image2',             # force format image file demuxer
        '-r', framerate,            # frame rate (fraction of second)
        '-i', filename_pattern,     # input image files
        '-vcodec', 'libx264',       # codec name
        '-c:v', 'libx264',          # codec name
        '-pix_fmt',                 # set pixel format
        'yuv420p',                  # pixel format
        f'{destination}/{filename_stub}.mp4'
    ]
    sleep(2)
    print('Compiling video..')
    subprocess.call(ffmpeg_command)
    print(f'Compiled: {destination}/{filename_stub}.mp4')
