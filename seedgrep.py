#!/usr/bin/python3

import os
import argparse
from nbt.nbt import *

parser = argparse.ArgumentParser(description="Search for Minecraft level.dats with a certain seed.", allow_abbrev=True)
parser.add_argument("-seed", metavar="seed", required=True, type=int, help="the seed to search for")
parser.add_argument("-root", metavar="root", default=".", type=str, help="the root directory to walk")

args = parser.parse_args()

targetseed = args.seed

for root, dirs, files in os.walk(args.root):
    for file in files:
        if file != "level.dat":
            continue
#       print("found level.dat file {}, checking...".format(file))
        nbtfile = NBTFile(file, "rb")
        fileseed = nbtfile["Data"]["RandomSeed"].value
        if fileseed == targetseed:
            print("found target seed {} in {}".format(targetseed, os.path.join(root, file)))

