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
from bfblib import plot_heat_cond
from bfblib import save_figures


def solve(pm):

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
    umf = bed.calc_umf()
    zexp = bed.calc_zexp(umf, us_h2)
    fig_geldart = bed.geldart_fig(rho_mix)

    # Feedstock
    feed = Feedstock(pm)
    t_devol = feed.devol_time(gas_h2.t)
    t_hc = feed.hc_time_vector()
    tk_hc = feed.heat_cond(t_hc)
    t_tinf = feed.get_time_tinf(t_hc, tk_hc)
    fig_heatcond = plot_heat_cond(t_hc, tk_hc, t_tinf)

    # Store results from calculations
    results = {
        'reactor': [ai],
        'gas_h2': [mw_h2, mu_h2, rho_h2, us_h2],
        'gas_n2': [mw_n2, mu_n2, rho_n2, us_n2],
        'gas_mix': [mu_graham, mu_herning, mw_mix, rho_mix],
        'bed': [umf, zexp],
        'feedstock': [t_devol, t_hc, tk_hc, t_tinf]
    }

    # Store plot figures
    figures = {
        'geldart': fig_geldart,
        'heatcond': fig_heatcond
    }

    return results, figures


def main(args):

    # Path of current working directory
    cwd = pathlib.Path.cwd()

    # Parameters for calculations
    pm = importlib.import_module(args.infile)

    # Solve for results and figures
    res, figs = solve(pm)

    # Print parameters and results
    print_parameters(pm)
    print_results(res)

    # Save plot figures to `results` directory
    save_figures(cwd, figs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module file')
    parser.add_argument('-c', '--clean', action='store_true', help='remove results folder')
    parser.add_argument('-s', '--solve', action='store_true', help='solve for BFB pyrolyzer')
    args = parser.parse_args()

    if args.clean:
        cwd = pathlib.Path.cwd()
        resdir = pathlib.Path(cwd, 'results')
        for file in resdir.iterdir():
            file.unlink()
        resdir.rmdir()
        print('\nDeleted `results` folder.\n')

    if args.solve:
        main(args)
