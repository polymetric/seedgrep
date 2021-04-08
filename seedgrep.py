#!/usr/bin/python3

import os
import argparse
from nbt.nbt import *

parser = argparse.ArgumentParser(description="Search for Minecraft level.dats and dump the seeds in them.", allow_abbrev=True)
parser.add_argument("-out", metavar="output file", default="seeds.txt", type=str, help="file to dump seeds to")
parser.add_argument("-dir", metavar="dir", default=".", type=str, help="the root directory to walk")
parser.add_argument("-verbose", default=False, action='store_true', help="print every seed to the console")
args = parser.parse_args()

outfile = open(args.out, "a")
absroot = os.path.abspath(args.dir)
worldsfound = 0

print("walking directory {}...".format(absroot))

for root, dirs, files in os.walk(absroot):
    for file in files:
        if file != "level.dat":
            continue
        file = os.path.join(root, file)
        worldsfound += 1
#       print("found level.dat file {}, checking...".format(file))
        nbtfile = NBTFile(file, "rb")
        fileseed = nbtfile["Data"]["RandomSeed"].value
        if args.verbose:
            print("found seed {} in {}".format(fileseed, file))
        outfile.write("{}: {}\n".format(file, fileseed))

print("done. found {} total worlds.".format(worldsfound))

