#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import numpy as np
from PIL import Image


def e2b(color):
    if color > 127 :
        return 1
    return 0


def print_color(F, B):
    F_color = 30 + e2b(F[0]) + e2b(F[1]) * 2 + e2b(F[2]) * 4
    B_color = 40 + e2b(B[0]) + e2b(B[1]) * 2 + e2b(B[2]) * 4
    print("\033[%d;%dm▀" % (F_color, B_color), end='')


def main(argv):
    if len(sys.argv) == 1 :
        print("Useage: %s pic_file" % sys.argv[0])
        return
    elif len(sys.argv) == 2 :
        pic_file_name = sys.argv[1]
    else :
        print("Useage: %s pic_file" % sys.argv[0])
        return

    print("%-20s%s" % ("pic file:", pic_file_name))

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

    ratio = width / shell_width
    print("%-20s%s" % ("ratio:", ratio))

    for i in range(0, height-1, int(2 * ratio + 0.5)) :
        for j in range(shell_width) :
            if i + int(ratio + 0.25) >= height :
                print_color(matrix[i][int(j * ratio)], [0, 0, 0])
                continue
            print_color(matrix[i][int(j * ratio)], matrix[i+int(ratio + 0.25)][int(j * ratio)])
        print("\033[39;49m")


if __name__ == "__main__":
    main(sys.argv)

