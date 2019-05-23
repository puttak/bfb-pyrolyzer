"""
here
"""

import argparse
import importlib
from bfblib import print_params


def main(args):
    params = importlib.import_module(args.infile)
    print_params(params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module')
    args = parser.parse_args()
    main(args)
