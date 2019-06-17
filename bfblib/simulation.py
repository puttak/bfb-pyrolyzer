import numpy as np

from .gas import Gas
from .bfb_model import BfbModel
from .particle_model import ParticleModel
from .pyrolysis_model import PyrolysisModel

from .printer import print_parameters
from .printer import print_gas_properties
from .printer import print_bfb_results
from .printer import print_particle_results
from .printer import print_pyrolysis_results

from .plotter import plot_geldart
from .plotter import plot_intra_particle_heat_cond
from .plotter import plot_umf_temps
from .plotter import plot_tdevol_temps
from .plotter import plot_ut_temps


class Simulation:

    def __init__(self, params, path=None):
        self._params = params
        self._path = path

    def run_params(self):

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(**self._params.gas)
        gas.calc_properties()

        # BFB model for fluidization
        bfb = BfbModel(gas, self._params)
        bfb.solve()

        # Particle model for biomass intra-particle heat conduction
        part = ParticleModel(gas, self._params)
        part.solve()

        # Pyrolysis model for biomass pyrolysis
        pyro = PyrolysisModel(gas, self._params)
        pyro.solve()

        # Print parameters to screen
        print(f"\n{' Parameters ':*^40}")
        print_parameters(self._params)

        # Print results to screen
        print(f"{' Results from Parameters ':*^40}")
        print_gas_properties(gas)
        print_bfb_results(bfb)
        print_particle_results(part)
        print_pyrolysis_results(pyro)

        # Create and save plot figures if path is defined
        if self._path is not None:
            plot_geldart(gas, self._params, self._path)
            plot_intra_particle_heat_cond(part, self._path)

    def run_temps(self):
        print(f"\n{' Simulate Temperatures ':*^40}\n")

        tk_ref = self._params.gas['tk']
        tk_min = self._params.case['tk'][0]
        tk_max = self._params.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        umfs_ergun = []
        umfs_wenyu = []
        uts_bed_ganser = []
        uts_bed_haider = []
        uts_bio_ganser = []
        uts_bio_haider = []
        uts_char_ganser = []
        uts_char_haider = []
        ts_devol = []

        for tk in tks:
            print(f'Run case at {tk} K ...')

            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(**self._params.gas)
            gas.tk = tk
            gas.calc_properties()

            # BFB model for fluidization
            bfb = BfbModel(gas, self._params)

            # Pyrolysis model for biomass pyrolysis
            pyro = PyrolysisModel(gas, self._params)
            t_devol = pyro.calc_devol_time()

            # Store results at temperature
            umfs_ergun.append(bfb.calc_umf_ergun())
            umfs_wenyu.append(bfb.calc_umf_wenyu())
            uts_bed_ganser.append(bfb.calc_ut_ganser()[0])
            uts_bed_haider.append(bfb.calc_ut_haider()[0])
            uts_bio_ganser.append(bfb.calc_ut_ganser()[1])
            uts_bio_haider.append(bfb.calc_ut_haider()[1])
            uts_char_ganser.append(bfb.calc_ut_ganser()[2])
            uts_char_haider.append(bfb.calc_ut_haider()[2])
            ts_devol.append(t_devol)

        plot_umf_temps(tks, umfs_ergun, umfs_wenyu, tk_ref, self._path)
        plot_ut_temps(tks, uts_bed_ganser, uts_bed_haider, uts_bio_ganser, uts_bio_haider, uts_char_ganser, uts_char_haider, tk_ref, self._path)
        plot_tdevol_temps(tks, ts_devol, tk_ref, self._path)

        print(f'Matplotlib figures saved to the `{self._path.name}` folder.\n')
