"""
here
"""

import argparse
import importlib
from bfblib import print_params
from bfblib import Gas


def main(args):
    params = importlib.import_module(args.infile)
    print_params(params)

    gas_h2 = Gas(params.gas[0], params.pgas, params.tgas)
    gas_n2 = Gas(params.gas[1], params.pgas, params.tgas)
    breakpoint()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module')
    args = parser.parse_args()
    main(args)
