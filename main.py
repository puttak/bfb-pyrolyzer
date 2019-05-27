"""
here
"""

import argparse
import importlib
import pathlib

from bfblib import Gas
from bfblib import GasMix
from bfblib import Particle

from bfblib import print_params
from bfblib import print_gas
from bfblib import print_gas_mix
from bfblib import print_bed_particle

from bfblib import save_figure


def main(args):
    params = importlib.import_module(args.infile)

    gas_h2 = Gas(params.gas[0], params.pgas, params.tgas, params.xgas[0])
    gas_n2 = Gas(params.gas[1], params.pgas, params.tgas, params.xgas[1])
    gas_mix = GasMix(gas_h2, gas_n2)

    bed_particle = Particle(params.dp, params.phi, params.rhos)
    geldart_fig = bed_particle.geldart_fig(gas_mix.rho, 200, 500)
    umf = bed_particle.umf(params.ep, gas_mix.mu_herning, gas_mix.rho)

    print_params(params)
    print_gas(gas_h2)
    print_gas(gas_n2)
    print_gas_mix(gas_mix)
    print_bed_particle(umf)

    cwd = pathlib.Path.cwd()
    save_figure('geldart', geldart_fig, cwd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module')
    args = parser.parse_args()
    main(args)
