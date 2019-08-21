import argparse
import importlib
import logging
import multiprocessing
import pathlib

from solve_parameters import SolveParameters
from plot_parameters import PlotParameters
from print_parameters import print_report

from solve_diameters import SolveDiameters
from plot_diameters import PlotDiameters

from solve_temperatures import SolveTemperatures
from plot_temperatures import PlotTemperatures


def solve_parameters(path):
    """
    Perform calculations for parameters file.
    """
    logging.info('Solve for case parameters')

    spec = importlib.util.spec_from_file_location('params', path / 'params.py')
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    solver = SolveParameters(params)
    solver.calc_results()
    print_report(params, solver, path)

    plotter = PlotParameters(solver, path)
    plotter.plot_geldart()
    plotter.plot_intra_particle_heat_cond()
    plotter.plot_umb_umf_ut()


def solve_diameters(path):
    """
    Perform calculations for a range of particle sizes.
    """
    logging.info('Solve for diameters')

    spec = importlib.util.spec_from_file_location('params', path / 'params.py')
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    solver = SolveDiameters(params)
    solver.calc_diameters()
    solver.calc_us()
    solver.calc_umf()
    solver.calc_ut()

    plotter = PlotDiameters(solver, path)
    plotter.plot_umf_bed()
    plotter.plot_ut_bed()
    plotter.plot_ut_biomass()


def solve_temperatures(path):
    """
    """
    logging.info('Solve for temperatures')

    spec = importlib.util.spec_from_file_location('params', path / 'params.py')
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    solver = SolveTemperatures(params)
    solver.get_temperatures()
    solver.calc_tv()
    solver.calc_us()
    solver.calc_us_umf()
    solver.calc_umb()
    solver.calc_umb_umf()
    solver.calc_umf()
    solver.calc_ut()

    plotter = PlotTemperatures(solver, path)
    plotter.plot_tv_temps()
    plotter.plot_umf_ratios_temps()
    plotter.plot_umb_umf_temps()
    plotter.plot_ut_temps()


def run_solvers(path):
    """
    """
    solve_parameters(path)
    solve_diameters(path)
    solve_temperatures(path)


def main():
    """
    Main entry point for program.
    """

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
