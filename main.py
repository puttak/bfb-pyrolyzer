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
from bfblib import print_gas_properties
from bfblib import print_gas_mix_properties
from bfblib import print_bfb_results
from bfblib import plot_geldart
from bfblib import plot_heat_cond
from bfblib import save_figures


def solve_gas(pm):

    # Gas properties
    gas = Gas(pm.gas['sp'][0], pm.gas['x'][0], pm)

    # BFB model
    bfb = BfbModel(gas, pm)
    ac = bfb.calc_inner_ac()
    us = bfb.calc_us(ac)
    umf_ergun = bfb.calc_umf_ergun(gas.mu)
    us_umf = bfb.calc_us_umf(us, umf_ergun)
    zexp = bfb.calc_zexp(umf_ergun, us)
    t_hc = bfb.build_time_vector()
    tk_hc = bfb.calc_trans_hc(t_hc, gas.tk)
    t_tkinf = bfb.calc_time_to_tinf(t_hc, tk_hc)
    t_devol = bfb.calc_devol_time()

    # Matplotlib figures
    fig_geldart = plot_geldart(gas, pm)
    fig_heatcond = plot_heat_cond(t_hc, tk_hc, t_tkinf)

    # Store results from calculations
    results = {
        'gas': gas,
        'ac': ac,
        'us': us,
        'umf_ergun': umf_ergun,
        'us_umf': us_umf,
        'zexp': zexp,
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
    print_gas_properties(gas)
    print_bfb_results(results)

    # Save plot figures to `results` directory
    cwd = pathlib.Path.cwd()
    save_figures(cwd, figures)


def solve_gas_mix(pm):

    # Gas mixture properties
    ngas = len(pm.gas['sp'])
    mus = []
    mws = []
    xs = []

    for i in range(ngas):
        gas = Gas(pm.gas['sp'][i], pm.gas['x'][i], pm)
        mus.append(gas.mu)
        mws.append(gas.mw)
        xs.append(gas.x)

    sp = '+'.join(pm.gas['sp'])
    gas = GasMix(sp, mus, mws, xs, pm)

    # BFB model
    bfb = BfbModel(gas, pm)
    ac = bfb.calc_inner_ac()
    us = bfb.calc_us(ac)
    umf_ergun = bfb.calc_umf_ergun(gas.mu_herning)
    us_umf = bfb.calc_us_umf(us, umf_ergun)
    zexp = bfb.calc_zexp(umf_ergun, us)
    t_hc = bfb.build_time_vector()
    tk_hc = bfb.calc_trans_hc(t_hc, gas.tk)
    t_tkinf = bfb.calc_time_to_tinf(t_hc, tk_hc)
    t_devol = bfb.calc_devol_time()

    # Matplotlib figures
    fig_geldart = plot_geldart(gas, pm)
    fig_heatcond = plot_heat_cond(t_hc, tk_hc, t_tkinf)

    # Store results from calculations
    results = {
        'gas': gas,
        'ac': ac,
        'us': us,
        'umf_ergun': umf_ergun,
        'us_umf': us_umf,
        'zexp': zexp,
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
    print_gas_mix_properties(gas)
    print_bfb_results(results)

    # Save plot figures to `results` directory
    cwd = pathlib.Path.cwd()
    save_figures(cwd, figures)


def main(args):
    # Parameters for calculations
    pm = importlib.import_module(args.infile)

    # Solve BFB model for a gas or gas mixture
    if len(pm.gas['sp']) > 1:
        solve_gas_mix(pm)
    else:
        solve_gas(pm)


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
