import argparse
import importlib
import logging
import multiprocessing
import pathlib

from solve_parameters import solve_parameters
from solve_diameters import solve_diameters
from solve_temperatures import solve_temperatures
from print_parameters import print_report

from plot_parameters import PlotParameters
from plot_diameters import PlotDiameters
from plot_temperatures import PlotTemperatures


def solve_params(params, path):
    """
    Perform calculations for parameters file.
    """

    logging.info('Solve for case parameters')
    results = solve_parameters(params)
    print_report(params, results, path)

    plotter = PlotParameters(params, results, path)
    plotter.plot_geldart()
    plotter.plot_intra_particle_heat_cond()
    plotter.plot_umb_umf_ut()


def solve_diams(params, path):
    """
    Perform calculations for a range of particle sizes.
    """
    logging.info('Solve for diameters')
    results = solve_diameters(params)

    plotter = PlotDiameters(params, results, path)
    plotter.plot_umf()
    plotter.plot_ut_bed()
    plotter.plot_ut_bio()


def solve_temps(params, path):
    """
    Perform calculations for a range of temperatures.
    """
    logging.info('Solve for temperatures')
    results = solve_temperatures(params)

    plotter = PlotTemperatures(params, results, path)
    plotter.plot_tv_temps()
    plotter.plot_umf_ratios_temps()
    plotter.plot_umb_umf_temps()
    plotter.plot_ut_temps()


def run_solvers(path):
    """
    Run all solvers.
    """
    spec = importlib.util.spec_from_file_location('params', path / 'params.py')
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    solve_params(params, path)
    solve_diams(params, path)
    solve_temps(params, path)


def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('project', help='project folder')
    parser.add_argument('-r', '--run', action='store_true', help='run parameters in serial')
    parser.add_argument('-mp', '--mprun', action='store_true', help='run parameters in parallel')
    parser.add_argument('-c', '--clean', action='store_true', help='remove generated files')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.info('Start BFB calculations')

    # Path to project folder which contains parameters for each case
    project_path = pathlib.Path(args.project)
    case_paths = [p for p in project_path.iterdir() if p.is_dir()]

    # Solve using parameters for each case (serial)
    if args.run:
        for path in case_paths:
            run_solvers(path)

    # Solve using parameters for each case (parallel)
    if args.mprun:
        with multiprocessing.Pool() as pool:
            pool.map(run_solvers, case_paths)

    # Clean up generated files from previous runs
    if args.clean:
        logging.info('Clean up generated files from previous runs')

        for path in case_paths:
            for file in path.iterdir():
                if not file.is_dir() and not file.suffix == '.py':
                    file.unlink()

        for file in project_path.iterdir():
            if file.suffix == '.pdf':
                file.unlink()

    logging.info('Done')


if __name__ == '__main__':
    main()
