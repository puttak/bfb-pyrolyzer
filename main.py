"""
Main driver for BFB model of a biomass pyrolysis reactor.
"""

import argparse
import importlib
import pathlib
from bfblib import Simulate


def main(args):

    # Get parameters as a Python module
    params = importlib.import_module(args.infile)

    # Run simulation based on parameters
    sim = Simulate()
    sim.load_parameters(params)
    sim.run()
    sim.print_parameters()
    sim.print_results()

    # Save results and figures to `results` folder
    # Create `results` folder in current directory if it doesn't exist
    if args.save:
        cwd = pathlib.Path.cwd()
        path = pathlib.Path(cwd, 'results')
        if not path.exists():
            path.mkdir()
        sim.save_results(path)
        sim.save_figures(path)

    # TODO implement simulation cases


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='path to parameters module file')
    parser.add_argument('-c', '--clean', action='store_true', help='remove results folder')
    parser.add_argument('-s', '--save', action='store_true', help='save results and figures')
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
