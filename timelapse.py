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
parser.add_argument('--name', '-n', help='Destination filename for timelapse.', default='timelapse')
parser.add_argument('--folder', '-f', help='Destination folder for timelapse.', default=None)
parser.add_argument('--webcam', '-w', help='Webcam (see `imagesnap -l` for name)', default=None)
parser.add_argument('--date', '-d', help='Add the date', action='store_true', default=False)
parser.add_argument('--compile', '-c', help='Compile (with ffmpeg)', action='store_true', default=False)

args = parser.parse_args()

# TODO: convert to f strings (python3 all the way)

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
    result = ("{0} day{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
        ("{0} hour{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
        ("{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "") if minutes else "") + \
        ("{0} second{1} ".format(
            seconds, "s" if seconds != 1 else "") if seconds else "")
    return result


def get_webcam(preferred='HD Pro Webcam C920'):
    webcam = 'FaceTime HD Camera'
    webcam_list = subprocess.check_output("imagesnap -l;", stderr=subprocess.STDOUT, shell=True)
    webcams = re.findall(r"\[(.*?)\]", str(webcam_list))[0::2]
    return preferred if preferred in webcams else webcams[0]

webcam = args.webcam or get_webcam()

def get_filepath(count, as_pattern=False):
    # import pudb; pudb.set_trace()
    filename = filename_stub
    if args.date:
        filename += '_' + created_date
    if as_pattern:
        pattern = '%{}'.format(str(padding).zfill(2))
        filename += '_{}d.jpg'.format(pattern)
    else:
        filename += '_{}.jpg'.format(str(count).zfill(padding))
    return destination + '/' + filename


def check_destination():
    if not os.path.isdir(destination):
        try:
            os.mkdir(destination)
        except OSError:
            print("Destination folder %s couldn't be created" % destination)

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
    print('{}/{}'.format(count, max_count))
    print('{} minutes recording time'.format(int((count*delay)/60)))
    print('{} second timelapse'.format(int(count/30)))
    count += 1
    sleep(delay - 1)

while not os.path.exists(get_filepath(max_count)):
    print('.')
    sleep(0.5)

if ffmpeg:
    filename_pattern = get_filepath(0, as_pattern=True)
    # filename_pattern ='/Users/tom/Downloads/bread_timelapse/timelapse_20190317_08-52/timelapse_%01d.jpg'
    print(filename_pattern)
    # ffmpeg_command = 'ffmpeg -f image2 -r 1/5 -i {} -c:v libx264 -pix_fmt yuv420p {}/{}.mp4'.format(filename_pattern, destination, filename_stub)
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
    print(ffmpeg_command)
    sleep(2)
    subprocess.call(ffmpeg_command)
