# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 13:49:13 2016

@author: default
"""
import time
import os
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS
import shutil
#import Image, ImageEnhance


dir_in = '/home/pi/airnef/incoming/'
dir_web = '/home/pi/PhotoFloat/web/albums/'

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

class session_class:
    def __init__(self):
        self.dir_org = dir_web + 'originals/'
        self.dir_wm = dir_web + 'watermarked/' 

def getsession(timestamp):
    return session_class()

def check_dir():
    for photo in os.listdir(dir_in):
        i = Image.open(dir_in + photo)
        timestamp = i._getexif()[36867]
        session = getsession(timestamp)
        im = Image.open(dir_in + photo)
        mark = Image.open('watermark.png')
        watermark(im, mark, 'scale', 1.0).save('watermarked.jpg')
        shutil.move(dir_in + photo, session.dir_org)
        shutil.move('watermarked.jpg' , session.dir_wm + photo)
        #  run code to re-scan                  

def main():
    while True:
        check_dir()
        time.sleep(3)

if __name__ == "__main__":
    main()
