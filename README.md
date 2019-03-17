# Webcam timelapse

This is a simple script that uses [imagesnap][imagesnap] to take images from the webcam every few seconds to create a timelapse. Initially this is just saved as a series of images, rather than a video.

Note: It is possible to use imagesnap itself to take images every few seconds:

`imagesnap -d 'FaceTime HD Camera' -t 2.0 image`

but I wanted a more configurable option.


## Installation

Works on a mac, due to imagesnap dependency, apologies to users of other platforms.

Install imagesnap

`brew install imagesnap`

Install [ffmpeg][ffmpeg]. Can take some time.. This is optional, for combining resulting images to video. You might have another preferred method to accomplish this.

`brew install ffmpeg`

Collect python dependencies

`pip -r requirements.txt`


## Usage

To record an image every 2min (120 seconds) for a duration of two and ahalf hours, and compile to mp4 video when complete:

`./timelapse.py 120 2hr30min -c`

If you need to change webcam, rather than defaulting to first found, use the 'list' parameter to determine available webcams: `./timelapse.py -l`.

To see other configuration options `./timelapse.py --help`.

[ffmpeg]: https://github.com/fluent-ffmpeg/node-fluent-ffmpeg/wiki/Installing-ffmpeg-on-Mac-OS-X
[imagesnap]: https://github.com/rharder/imagesnap
