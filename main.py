"""
Main driver for BFB model of a biomass pyrolysis reactor.
"""

import argparse
import importlib
import pathlib

from bfblib import Simulation


def main(args):

    # Get parameters from a Python module
    infile = args.infile.replace('/', '.')[:-3]
    params = importlib.import_module(infile)

    # Initialize simulation with parameters
    sim = Simulation(params)

    # Run simulation or a simulation case based on command line option
    if args.temps:
        sim.run_temps()
        path = pathlib.Path.cwd() / 'results'
        if not path.exists():
            path.mkdir()
        sim.save_results(path, case=True)
    else:
        sim.run_params()
        sim.print_parameters()
        sim.print_results()

        # Save results and figures to `results` folder.
        if args.save:
            path = pathlib.Path.cwd() / 'results'
            if not path.exists():
                path.mkdir()
            sim.save_results(path)
            sim.save_figures(path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module file')
    parser.add_argument('-c', '--clean', action='store_true', help='remove results folder')
    parser.add_argument('-s', '--save', action='store_true', help='save results and figures')
    parser.add_argument('-t', '--temps', action='store_true', help='run temperatures case')
    args = parser.parse_args()

    if args.clean:
        path = pathlib.Path.cwd() / 'results'
        for file in path.iterdir():
            file.unlink()
        path.rmdir()
        print('\nDeleted `results` folder.\n')
    else:
        main(args)
