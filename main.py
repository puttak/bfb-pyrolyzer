"""
here
"""

import argparse
import importlib
import pathlib

from bfblib import Gas
from bfblib import GasMix
from bfblib import Reactor
from bfblib import Bed

from bfblib import print_parameters
from bfblib import print_reactor
from bfblib import print_gas
from bfblib import print_gas_mix
from bfblib import print_bed_particle

from bfblib import save_figure


def main(args):
    cwd = pathlib.Path.cwd()

    # Parameters
    params = importlib.import_module(args.infile)
    print_parameters(params)

    # Reactor
    rct = Reactor(params)
    print_reactor(rct)

    # Gas and Gas Mixture
    gas_h2 = Gas(params.gas[0], params.xgas[0], params, rct)
    gas_n2 = Gas(params.gas[1], params.xgas[1], params, rct)
    gas_mix = GasMix(gas_h2, gas_n2)
    print_gas(gas_h2)
    print_gas(gas_n2)
    print_gas_mix(gas_mix)

    # Bed
    bed = Bed(params, gas_mix)
    geldart_fig = bed.geldart_fig(200, 500)
    print_bed_particle(bed.umf, gas_h2.us)
    save_figure('geldart', geldart_fig, cwd)

    # Feed
    # stuff goes here


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module')
    args = parser.parse_args()
    main(args)
