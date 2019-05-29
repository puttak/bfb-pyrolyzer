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
    a_inner = rct.a_inner

    # Gas H2
    gas_h2 = Gas(pm.gas['species'][0], pm.gas['x'][0], pm, a_inner)
    mw_h2 = gas_h2.mw
    mu_h2 = gas_h2.mu
    rho_h2 = gas_h2.rho
    us_h2 = gas_h2.us

    # Gas N2
    gas_n2 = Gas(pm.gas['species'][1], pm.gas['x'][1], pm, a_inner)
    mw_n2 = gas_n2.mw
    mu_n2 = gas_n2.mu
    rho_n2 = gas_n2.rho
    us_n2 = gas_n2.us

    # Gas Mixture of H2 and N2
    gas_mix = GasMix(gas_h2, gas_n2)
    mu_graham = gas_mix.mu_graham
    mu_herning = gas_mix.mu_herning
    mw_mix = gas_mix.mw
    rho_mix = gas_mix.rho

    # Bed
    bed = Bed(pm, mu_herning, rho_mix)
    geldart_fig = bed.geldart_fig(rho_mix, 200, 500)
    umf = bed.umf
    zexp = bed.zexp(umf, us_h2)

    # Feedstock
    feed = Feedstock(pm)
    tv = feed.devol_time(gas_h2.temp)

    # ---------- Print ----------

    # Print parameters from the `params` module
    print_parameters(pm)

    # Print `results` dictionary
    results = {
        'reactor': [a_inner],
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
    parser.add_argument('infile', help='path to parameters module file')
    args = parser.parse_args()
    main(args)
