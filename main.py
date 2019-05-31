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
from bfblib import Feedstock

from bfblib import print_parameters
from bfblib import print_results

from bfblib import save_figure


def main(args):
    cwd = pathlib.Path.cwd()

    # ---------- Parameters ----------

    pm = importlib.import_module(args.infile)

    # ---------- Results ----------

    # Reactor
    rct = Reactor(pm)
    ai = rct.calc_ai()

    # Gas H2
    gas_h2 = Gas(pm.gas['species'][0], pm.gas['x'][0], pm.gas['p'], pm.gas['t'])
    mw_h2 = gas_h2.mw
    mu_h2 = gas_h2.calc_mu()
    rho_h2 = gas_h2.calc_rho()
    us_h2 = gas_h2.calc_us(ai, pm.gas['q'])

    # Gas N2
    gas_n2 = Gas(pm.gas['species'][1], pm.gas['x'][1], pm.gas['p'], pm.gas['t'])
    mw_n2 = gas_n2.mw
    mu_n2 = gas_n2.calc_mu()
    rho_n2 = gas_n2.calc_rho()
    us_n2 = gas_n2.calc_us(ai, pm.gas['q'])

    # Gas Mixture of H2 and N2
    gas_mix = GasMix([mu_h2, mu_n2], [mw_h2, mw_n2], [gas_h2.x, gas_n2.x], pm.gas['p'], pm.gas['t'])
    mu_graham = gas_mix.calc_mu('graham')
    mu_herning = gas_mix.calc_mu('herning')
    mw_mix = gas_mix.calc_mw()
    rho_mix = gas_mix.calc_rho(mw_mix)

    # Bed
    bed = Bed(pm, mu_herning, rho_mix)
    geldart_fig = bed.geldart_fig(rho_mix, 200, 500)
    umf = bed.calc_umf()
    zexp = bed.calc_zexp(umf, us_h2)

    # Feedstock
    feed = Feedstock(pm)
    tv = feed.devol_time(gas_h2.t)

    # ---------- Print ----------

    # Print parameters from the `params` module
    print_parameters(pm)

    # Print `results` dictionary
    results = {
        'reactor': [ai],
        'gas_h2': [mw_h2, mu_h2, rho_h2, us_h2],
        'gas_n2': [mw_n2, mu_n2, rho_n2, us_n2],
        'gas_mix': [mu_graham, mu_herning, mw_mix, rho_mix],
        'bed': [umf, zexp],
        'feedstock': [tv]
    }
    print_results(results)

    # ---------- Save Figures ----------

    # Save plot figures to `results/` directory
    save_figure('geldart', geldart_fig, cwd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', help='path to parameters module file')
    parser.add_argument('-c', '--clean', action='store_true', help='remove results folder')
    args = parser.parse_args()

    if args.infile is not None:
        main(args)

    if args.clean:
        cwd = pathlib.Path.cwd()
        results_dir = pathlib.Path(cwd, 'results')
        for file in results_dir.iterdir():
            file.unlink()
        results_dir.rmdir()
