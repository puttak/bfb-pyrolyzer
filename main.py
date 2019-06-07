"""
Main driver for BFB pyrolyzer model.
"""

import argparse
import importlib
import pathlib

from bfblib import Gas
from bfblib import GasMix
from bfblib import BfbModel

from bfblib import print_parameters
from bfblib import print_results
from bfblib import plot_geldart
from bfblib import plot_heat_cond
from bfblib import save_figures


def solve(pm):

    # Gas properties for H2 and N2
    gas_h2 = Gas(pm.gas['sp'][0], pm.gas['x'][0], pm.gas['p'], pm.gas['q'], pm.gas['tk'])
    gas_n2 = Gas(pm.gas['sp'][1], pm.gas['x'][1], pm.gas['p'], pm.gas['q'], pm.gas['tk'])

    # Gas mixture properties
    mus = (gas_h2.mu, gas_n2.mu)
    mws = (gas_h2.mw, gas_n2.mw)
    xs = (gas_h2.x, gas_n2.x)
    gas_mix = GasMix(mus, mws, xs, pm.gas['p'], pm.gas['q'], pm.gas['tk'])

    # BFB model
    bfb = BfbModel(gas_mix, pm)
    bfb.calc_umf_ergun('herning')
    bfb.calc_zexp('ergun')

    # Matplotlib figures
    fig_geldart = plot_geldart(bfb, gas_mix)
    fig_heatcond = plot_heat_cond(bfb)

    # Store results from calculations
    results = {
        'reactor': [bfb.ac_rct],
        'gas_h2': [gas_h2.mw, gas_h2.mu, gas_h2.rho, bfb.us_bed],
        'gas_n2': [gas_n2.mw, gas_n2.mu, gas_n2.rho, bfb.us_bed],
        'gas_mix': [gas_mix.mu_graham, gas_mix.mu_herning, gas_mix.mw, gas_mix.rho],
        'bed': [bfb.umf_ergun_bed, bfb.zexp_bed],
        'feedstock': [bfb.tv_feed, bfb.t_hc, bfb.tk_hc, bfb.t_tinf]
    }

    # Store plot figures
    figures = {
        'geldart': fig_geldart,
        'heatcond': fig_heatcond
    }

    return results, figures


def main(args):
    # Parameters for calculations
    pm = importlib.import_module(args.infile)

    res, figs = solve(pm)

    # Print parameters and results
    print_parameters(pm)
    print_results(res)

    # Save plot figures to `results` directory
    cwd = pathlib.Path.cwd()
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
