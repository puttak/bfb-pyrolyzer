"""
Main driver for BFB model of a biomass pyrolysis reactor.
"""

import argparse
import importlib
import pathlib

from bfblib import Gas
from bfblib import GasMix
from bfblib import BfbModel

from bfblib import print_parameters
from bfblib import print_bfb_results

from bfblib import plot_geldart
from bfblib import plot_heat_cond
from bfblib import save_figures


def solve(pm):

    # Gas species is a list (gas mixture) or string (single gas)
    sp = pm.gas['sp']

    # Gas properties for a single gas component or a gas mixture
    # Note that gas mixture uses the Herning calculation method
    if type(sp) is list:
        mus = []
        mws = []
        xs = []

        for i in range(len(sp)):
            gas = Gas(sp[i], pm.gas['x'][i], pm)
            mus.append(gas.mu)
            mws.append(gas.mw)
            xs.append(gas.x)

        gas = GasMix(mus, mws, xs, pm)
        mug = gas.mu_herning
    elif type(sp) is str:
        gas = Gas(sp, pm.gas['x'], pm)
        mug = gas.mu

    # BFB model
    bfb = BfbModel(gas, pm)
    ac = bfb.calc_inner_ac()
    us = bfb.calc_us(ac)

    umf_ergun = bfb.calc_umf_ergun(mug)
    us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
    zexp_ergun = bfb.calc_zexp(umf_ergun, us)

    umf_wenyu = bfb.calc_umf_wenyu(mug)
    us_umf_wenyu = bfb.calc_us_umf(us, umf_wenyu)
    zexp_wenyu = bfb.calc_zexp(umf_wenyu, us)

    t_hc = bfb.build_time_vector()
    tk_hc = bfb.calc_trans_hc(t_hc, gas.tk)
    t_tkinf = bfb.calc_time_to_tinf(t_hc, tk_hc)
    t_devol = bfb.calc_devol_time()

    # Matplotlib figures
    fig_geldart = plot_geldart(gas, pm)
    fig_heatcond = plot_heat_cond(t_hc, tk_hc, t_tkinf)

    # Store results from calculations
    results = {
        'gas_mw': gas.mw,
        'gas_mu': mug,
        'gas_rho': gas.rho,
        'ac': ac,
        'us': us,
        'umf_ergun': umf_ergun,
        'us_umf_ergun': us_umf_ergun,
        'zexp_ergun': zexp_ergun,
        'umf_wenyu': umf_wenyu,
        'us_umf_wenyu': us_umf_wenyu,
        'zexp_wenyu': zexp_wenyu,
        't_tkinf': t_tkinf,
        't_devol': t_devol
    }

    # Store plot figures
    figures = {
        'geldart': fig_geldart,
        'heatcond': fig_heatcond
    }

    # Print parameters and results
    print_parameters(pm)
    print_bfb_results(results)

    # Save plot figures to `results` directory
    cwd = pathlib.Path.cwd()
    save_figures(cwd, figures)


def main(args):

    # Get parameters and solve BFB model
    pm = importlib.import_module(args.infile)
    solve(pm)


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
