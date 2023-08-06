#!python

import argparse

from mt import cv, np

def main(args):
    imm = cv.immload(args.imm_file)
    print("Image path: {}".format(args.imm_file))
    print("Pixel format: {}".format(imm.pixel_format))
    print("Meta:")
    print(imm.meta)
    print("Press any key to exit.")
    cv.namedWindow('image')
    cv.imshow('image', imm.image)
    cv.waitKey(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('imm_file', type=str,
                        help="The file to view.")
    args = parser.parse_args()    
    main(args)
