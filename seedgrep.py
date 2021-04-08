#!/usr/bin/python3

import os
import argparse
from nbt.nbt import *

targetseed = 1337

for root, dirs, files in os.walk("."):
    for file in files:
        if file != "level.dat":
            continue
#       print("found level.dat file {}, checking...".format(file))
        nbtfile = NBTFile(file, "rb")
        fileseed = nbtfile["Data"]["RandomSeed"].value
        if fileseed == targetseed:
            print("found target seed {} in {}".format(targetseed, os.path.join(root, file)))

