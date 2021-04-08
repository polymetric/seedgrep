#!/usr/bin/python3

import os
import argparse
import traceback
from nbt.nbt import *
import timeit

# from https://gist.github.com/hanleybrand/5224673
def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

parser = argparse.ArgumentParser(description="Search for Minecraft level.dats and dump the seeds in them.", allow_abbrev=True)
parser.add_argument("-out", metavar="output file", default="seeds.txt", type=str, help="file to dump seeds to")
parser.add_argument("-dir", metavar="dir", default=".", type=str, help="the root directory to walk")
parser.add_argument("-verbose", default=False, action='store_true', help="print every seed to the console")
args = parser.parse_args()

# TODO make this overwrite the output file, with a catch warning
outfile = open(args.out, "a")
absroot = os.path.abspath(args.dir)
worldsfound = 0

print("walking directory {}...".format(absroot))

start = timeit.default_timer()

for root, dirs, files in os.walk(absroot):
    for file in files:
        if file != "level.dat" and file != "level.dat_old":
            continue
        worldsfound += 1
        file = os.path.join(root, file)
        try:
            nbtfile = NBTFile(file, "rb")
            fileseed = nbtfile["Data"]["RandomSeed"].value
            if args.verbose:
                print("found seed {} in {}".format(fileseed, file))
            outfile.write("{}: {}\n".format(file, fileseed))
        except Exception as e:
            if args.verbose:
                # TODO make this actually handle the error properly.
                # a lot of these errors seem to come from level.dats which
                # are missing the seed tag. probably because it was changed at some point
                pass
#               print("error occurred on file {}:".format(file))
#               print(traceback.format_exc())
#               print(e)

print("done. found {} total worlds in {:.3f}s.".format(worldsfound, timeit.default_timer()-start))

