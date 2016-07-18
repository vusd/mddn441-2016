#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import shutil
import os
import sys
import urllib
from tqdm import tqdm

local_image = "inputs/wasp.jpg"

def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)    

def ensure_directory_cleaned(dirname):
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")
    # make a new outputs directory
    os.mkdir("outputs")

def download_a_file(remote_file, local_file):
    urllib.urlretrieve(remote_file, local_file)

def download_files():
    ensure_directory_exists("inputs")
    download_a_file("http://www.victoria.ac.nz/__data/assets/image/0004/359563/wasp-banner-white.jpg", local_image)

def build_movie_images():
    ensure_directory_exists("outputs")
    # horizontal pan
    for i in tqdm(range(60)):
        offset = 300 + 20 * i
        outfile = "outputs/img_{:03d}.png".format(i)
        command = "convert {} -crop 440x220+{}+200 {}".format(local_image, offset, outfile)
        os.system(command)

def build_movie_from_images(movie_file):
    ensure_directory_exists("movies")
    ffmpeg_sequence = "outputs/img_%3d.png"
    command = "ffmpeg -r 20 -f image2 -i {} -c:v libx264 -crf 20 -pix_fmt yuv420p -tune fastdecode -y -tune zerolatency -profile:v baseline {}\n".format(ffmpeg_sequence, movie_file)
    os.system(command)

if __name__ == "__main__":
    # argparse
    parser = argparse.ArgumentParser(description='Make a movie')
    parser.add_argument('steps', nargs='*', help='Which steps to run', default=["download", "render"])
    args = parser.parse_args()


    for step in args.steps:
        if step == "download":
            print("Downloading files")
            download_files()
        elif step == "render":
            print("Rendering movie")
            build_movie_images()
            build_movie_from_images("movies/bee_pan.mp4")
        else:
            print("Unknown step: {}".format(step))
            sys.exit(1)
