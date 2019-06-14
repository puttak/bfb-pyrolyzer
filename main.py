"""
Main driver for BFB model of a biomass pyrolysis reactor.
"""

import argparse
import importlib
import pathlib
from bfblib import Simulation
from bfblib import print_parameters
from bfblib import print_results


def main(args):

    # Get parameters as a Python module
    infile = args.infile.replace('/', '.')[:-3]
    params = importlib.import_module(infile)

    if args.temps:
        # Run simulation case for temperatures
        sim = Simulation(params)
        sim.run_temps()
        path = pathlib.Path(pathlib.Path.cwd(), 'results')
        if not path.exists():
            path.mkdir()
        sim.save_results(path, case=True)
    else:
        # Run simulation based on BFB model parameters
        sim = Simulation(params)
        sim.run_params()
        print_parameters(params)
        print_results(sim.results)

        # Save results and figures to `results` folder
        # Create `results` folder in current directory if it doesn't exist
        if args.save:
            path = pathlib.Path(pathlib.Path.cwd(), 'results')
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
        cwd = pathlib.Path.cwd()
        resdir = pathlib.Path(cwd, 'results')
        for file in resdir.iterdir():
            file.unlink()
        resdir.rmdir()
        print('\nDeleted `results` folder.\n')
    else:
        main(args)
