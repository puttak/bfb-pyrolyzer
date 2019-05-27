"""
Main driver for BFB pyrolyzer model.
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
from bfblib import print_bed_calcs

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
    gas_h2 = Gas(params.gas[0], params.x_gas[0], params, rct)
    gas_n2 = Gas(params.gas[1], params.x_gas[1], params, rct)
    gas_mix = GasMix(gas_h2, gas_n2)
    print_gas(gas_h2)
    print_gas(gas_n2)
    print_gas_mix(gas_mix)

    # Bed Calculations
    bed = Bed(params)
    umf = bed.umf(gas_mix.mu_herning, gas_mix.rho)
    zexp = bed.zexp(params.di, gas_mix.rho, umf, gas_h2.us)
    print_bed_calcs(umf, gas_h2.us, zexp)

    geldart_fig = bed.geldart_fig(gas_mix.rho, 200, 500)
    save_figure('geldart', geldart_fig, cwd)

    # Feed Calculations
    # stuff goes here


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module')
    args = parser.parse_args()
    main(args)
