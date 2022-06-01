import os
import re
import shlex
import subprocess
from enum import Enum
from django.conf import settings



def get_resolution_config(key):
    resolutions = {
        '360': '480:360',
        '480': '640:480',
        '720': '1280:720',
        '1080': '1920:1080'
    }

    return resolutions[key]



# A path you want to save a random key to your local machine
# save_to = '/home/public_html/"PATH TO THE KEY DIRECTORY"/key'

# A URL (or a path) to access the key on your website
# url = 'http://localhost:8000/media/enc.key'
# or 
# url = '/"PATH TO THE KEY DIRECTORY"/key';

# hls = video.hls(Formats.h264())
# hls.encryption(save_to, url)
# hls.auto_generate_representation()
# hls.output('http://localhost:8000/media/video/1/hls/360/hls.m3u8')


def get_file_path(path):
    for file in os.scandir(path):
        if file.is_file() and file.name.endswith('.mp4'):
            return file.path

        else:
            print('No files in the raw directory')


def get_hls_path(path):
    for file in os.scandir(path):
        print(file.name)
        if file.is_file() and file.name.endswith('.m3u8'):
            return file.path
            break
        else:
            continue


def convert_to_hls(video_file, dest_path):
    enc_path = os.path.join(settings.BASE_DIR, "enc.keyinfo")
    for folder_path in os.scandir(dest_path):
        hls_path = os.path.join(folder_path.path, 'hls.m3u8')
        res = get_resolution_config(folder_path.name)
        hls_cmd = shlex.split(
            f"ffmpeg -i {video_file} -c:a aac -ar 44100 -ac 1 -vf scale={res} -hls_key_info_file {enc_path}\
                -preset medium -crf 18 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {hls_path}", 
            posix=False
        )
        print(hls_cmd)
        status = subprocess.run(hls_cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        print(status.stderr)

