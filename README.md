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


## Usage

Use imagesnap to determine available webcams via `imagesnap -l`.

[ffmpeg]: https://github.com/fluent-ffmpeg/node-fluent-ffmpeg/wiki/Installing-ffmpeg-on-Mac-OS-X
[imagesnap]: https://github.com/rharder/imagesnap
