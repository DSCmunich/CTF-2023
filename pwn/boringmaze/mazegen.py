#!/usr/bin/python3

def convert_decode(ifilename, ofilename):
    with open(ifilename) as ifile:
        lines = ifile.readlines()
    output = ""
    for l in lines:
        i = 0
        while i < len(l):
            output += l[i:i+2]
            i += 3
    with open(ofilename, "w") as ofile:
        ofile.write(output)

convert_decode("maze_dcode.txt", "maze_newline.txt")