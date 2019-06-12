"""
Main driver for BFB model of a biomass pyrolysis reactor.
"""

import argparse
import importlib
import pathlib
from bfblib import Simulate


def main(args):

    # Path to `results` folder, create path if doesn't exist
    cwd = pathlib.Path.cwd()
    results_path = pathlib.Path(cwd, 'results')
    if not results_path.exists():
        results_path.mkdir()

    # Get parameters as a Python module
    params = importlib.import_module(args.infile)

    # Run simulation based on parameters
    sim = Simulate(params)
    sim.save_figures(results_path)

    # TODO implement simulation cases


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
