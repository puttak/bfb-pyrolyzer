import matplotlib.pyplot as plt
import numpy as np

from .gas import Gas
from .bfb_model import BfbModel
from .particle_model import ParticleModel
from .pyrolysis_model import PyrolysisModel

from .printer import print_header
from .printer import print_parameters
from .printer import print_gas_properties
from .printer import print_bfb_results
from .printer import print_particle_results
from .printer import print_pyrolysis_results

from .plotter import plot_geldart
from .plotter import plot_intra_particle_heat_cond


class Simulation:

    def __init__(self, params, path=None):
        self.params = params
        self.path = path
        self.results = {}
        self.figures = {}
        self.results_case = []

    def run_params(self):

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(**self.params.gas)
        gas.calc_properties()

        # BFB model for fluidization
        bfb = BfbModel(gas, self.params)
        bfb.solve_params()

        # Particle model for biomass intra-particle heat conduction
        part = ParticleModel(gas, self.params)
        part.solve()

        # Pyrolysis model for biomass pyrolysis
        pyro = PyrolysisModel(gas, self.params)
        pyro.solve()

        # Print parameters to screen
        print_header('Parameters')
        print_parameters(self.params)

        # Print results to screen
        print_header('Results')
        print_gas_properties(gas)
        print_bfb_results(bfb)
        print_particle_results(part)
        print_pyrolysis_results(pyro)

        # Create and save plot figures if path is defined
        if self.path is not None:
            plot_geldart(gas, self.params, self.path)
            plot_intra_particle_heat_cond(part, self.path)

    def run_temps(self):

        print('>>>>>>>> Simulate Temperatures <<<<<<<<')
        tk_min = self.params.case['tk'][0]
        tk_max = self.params.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        umf_ergun = []
        umf_wenyu = []

        for tk in tks:
            print(f'Running case at {tk} K ...')

            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(**self.params.gas)
            gas.tk = tk
            gas.calc_properties()

            # BFB model for fluidization
            bfb = BfbModel(gas, self.params)

            # Store Umf at temperature
            umf_ergun.append(bfb.calc_umf_ergun(gas.mu))
            umf_wenyu.append(bfb.calc_umf_wenyu(gas.mu))

            # # Particle model for biomass intra-particle heat conduction
            # prt = ParticleModel(gas, self.params)
            # prt.solve()

            # # Pyrolysis model for biomass pyrolysis
            # pyro = PyrolysisModel(gas, self.params)
            # pyro.solve()

            # # Store results for temperature
            # results = {'tk': tk, **bfb.results, **prt.results, **pyro.results}
            # self.results_case.append(results)

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(tks, umf_ergun, '.-', label='Ergun')
        ax.plot(tks, umf_wenyu, '.-', label="WenYu")
        ax.fill_between(tks, umf_ergun, umf_wenyu, facecolor='0.9')
        ax.grid(color='0.9')
        ax.legend(loc='best')
        ax.set_frame_on(False)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Umf [m/s]')
        ax.tick_params(color='0.9')

        plt.show()
