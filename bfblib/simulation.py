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
        gas = Gas(self._params)

        # BFB model for fluidization
        bfb = BfbModel(gas, self._params)

        # Particle model for biomass intra-particle heat conduction
        part = ParticleModel(gas, self._params)

        # Pyrolysis model for biomass pyrolysis
        pyro = PyrolysisModel(gas, self._params)

        # Print parameters and results to screen
        print(f"\n{' Parameters ':*^40}")
        print_parameters(self._params)

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

        # Store Umf at each temperature from Ergun and WenYu equations
        umf_ergun = []
        umf_wenyu = []

        # Store Ut at each temperature from Ganser and Haider equations
        ut_bed_ganser = []
        ut_bed_haider = []
        ut_bio_ganser = []
        ut_bio_haider = []
        ut_char_ganser = []
        ut_char_haider = []

        # Store devolatilization time for each temperature
        ts_devol = []

        for tk in tks:
            print(f'Run case at {tk} K ...')

            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(self._params)
            gas.update_temperature(tk)

            # BFB model for fluidization
            bfb = BfbModel(gas, self._params)

            # Pyrolysis model for biomass pyrolysis
            pyro = PyrolysisModel(gas, self._params)

            # Append results for each temperature
            umf_ergun.append(bfb.umf_ergun)
            umf_wenyu.append(bfb.umf_wenyu)
            ut_bed_ganser.append(bfb.ut_bed_ganser)
            ut_bed_haider.append(bfb.ut_bed_haider)
            ut_bio_ganser.append(bfb.ut_bio_ganser)
            ut_bio_haider.append(bfb.ut_bio_haider)
            ut_char_ganser.append(bfb.ut_char_ganser)
            ut_char_haider.append(bfb.ut_char_haider)
            ts_devol.append(pyro.t_devol)

        uts_ganser = {'bed': ut_bed_ganser, 'bio': ut_bio_ganser, 'char': ut_char_ganser}
        uts_haider = {'bed': ut_bed_haider, 'bio': ut_bio_haider, 'char': ut_char_haider}

        plot_umf_temps(tks, umf_ergun, umf_wenyu, tk_ref, self._path)
        plot_ut_temps(tks, uts_ganser, uts_haider, self._path)
        plot_tdevol_temps(tks, ts_devol, tk_ref, self._path)

        print(f'Matplotlib figures saved to the `{self._path.name}` folder.\n')
