#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import getopt
import numpy as np
from PIL import Image


def e2b(color):
    if color > 127 :
        return 1
    return 0


def print_color(motd, F, B):
    F_color = 30 + e2b(F[0]) + e2b(F[1]) * 2 + e2b(F[2]) * 4
    B_color = 40 + e2b(B[0]) + e2b(B[1]) * 2 + e2b(B[2]) * 4
    motd.write("\033[%d;%dm▀" % (F_color, B_color))
    

def usage():
    print("Useage: %s [-w width] pic_file" % sys.argv[0])


def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    if len(args) != 1:
        usage()
        sys.exit(2)
    pic_file_name = args[0]
    print("%-20s%s" % ("pic file:", pic_file_name))

    motd = open("/etc/motd", mode = "w")

    image = Image.open(pic_file_name)
    matrix = np.asarray(image)
    print("%-20s%s" % ("type matrix:", type(matrix)))
    print("%-20s%s" % ("shape matrix:", matrix.shape))
    print("%-20s%s" % ("Dimension matrix:", len(matrix.shape)))

    if len(matrix.shape) < 3 :
        print("not color pic!")
        return

    height = matrix.shape[0]
    width  = matrix.shape[1]
    print("%-20s%s" % ("height:", height))
    print("%-20s%s" % ("width:", width))

    shell_height, shell_width = os.popen('stty size', 'r').read().split()
    shell_width = int(shell_width)
    print("%-20s%s" % ("shell_width:", shell_width))

    loop_width = shell_width
    for o, a in opts:
        if o == "-w":
            loop_width = int(a)

    if loop_width > shell_width:
        loop_width = shell_width

    print("%-20s%s" % ("loop_width:", loop_width))

    ratio = width / loop_width
    print("%-20s%s" % ("ratio:", ratio))

    for i in range(0, height-1, int(2 * ratio + 0.5)) :
        for j in range(loop_width) :
            if i + int(ratio + 0.25) >= height :
                print_color(motd, matrix[i][int(j * ratio)], [0, 0, 0])
                continue
            print_color(motd, matrix[i][int(j * ratio)], matrix[i+int(ratio + 0.25)][int(j * ratio)])
        motd.write("%c[39;49m\n" % 0x1B)

    motd.close()


if __name__ == "__main__":
    main(sys.argv)

