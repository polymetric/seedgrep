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
parser.add_argument("-seed", metavar="seed", required=False, default=None, type=str, help="optionally filter seeds before dumping them")
parser.add_argument("-out", metavar="output file", default="seeds.txt", type=str, help="file to dump seeds to")
parser.add_argument("-dir", metavar="dir", default=".", type=str, help="the root directory to walk")
parser.add_argument("-verbose", default=False, action='store_true', help="print every seed to the console")
parser.add_argument("-interactive", default=False, action='store_true', help="use interactive mode")
args = parser.parse_args()
if args.interactive:
    args.dir = None
    while args.dir == None or os.path.exists(args.dir) == False:
        args.dir = os.path.join(input("enter the folder or drive to scan (for example, C:): "), "/")
        if os.path.exists(args.dir) == False:
            print("invalid drive/folder, please try something else")
    args.seed = input("enter the seed to search for (nothing means output all seeds): ")
    if args.seed == "":
        args.seed = None

if args.seed != None:
    try:
        targetseed = int(args.seed)
    except:
        targetseed = java_string_hashcode(args.seed)

# TODO make this overwrite the output file, with a catch warning
outfile = open(args.out, "a")
absroot = os.path.abspath(args.dir)
worldsfound = 0
start = timeit.default_timer()

for root, dirs, files in os.walk(absroot):
    for file in files:
#       if file != "level.dat" and file != "level.dat_old":
        if file != "level.dat":
            continue
        file = os.path.join(root, file)
        try:
            nbtfile = NBTFile(file, "rb")
            fileseed = nbtfile["Data"]["RandomSeed"].value
            if args.seed != None and fileseed != targetseed:
                continue
            worldsfound += 1
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

print("done. found {} total worlds in {:.3f}s, dumped to file {}".format(worldsfound, timeit.default_timer()-start, args.out))

