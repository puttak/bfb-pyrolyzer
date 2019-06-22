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
        gas = Gas(self._params.gas)

        # BFB model for fluidization
        bfb = BfbModel(gas, self._params)
        ac = bfb.ac
        us = bfb.calc_us()
        tdh = bfb.calc_tdh(us)

        umf = bfb.calc_umf()
        us_umf = bfb.calc_us_umf(umf, us)
        zexp = bfb.calc_zexp(umf, us)

        ut_bed = bfb.calc_ut_bed()
        ut_bio = bfb.calc_ut_biomass()
        ut_char = bfb.calc_ut_char()

        results_bfb = (ac, us, tdh, umf, us_umf, zexp, ut_bed, ut_bio, ut_char)

        # Particle model for biomass intra-particle heat conduction
        part = ParticleModel(gas, self._params)
        t_hc = part.build_time_vector()
        tk_hc = part.calc_trans_hc(t_hc, gas.tk)
        t_tkinf = part.calc_time_tkinf(t_hc, tk_hc)

        results_part = (t_hc, tk_hc, t_tkinf)

        # Pyrolysis model for biomass pyrolysis
        pyro = PyrolysisModel(gas, self._params)
        t_devol = pyro.calc_devol_time()

        results_pyro = (t_devol,)

        # Print parameters and results to screen
        print(f"\n{' Parameters ':*^40}")
        print_parameters(self._params)

        print(f"{' Results from Parameters ':*^40}")
        print_gas_properties(gas)
        print_bfb_results(results_bfb)
        print_particle_results(results_part)
        print_pyrolysis_results(results_pyro)

        # Create and save plot figures if path is defined
        if self._path is not None:
            plot_geldart(gas, self._params, self._path)
            plot_intra_particle_heat_cond(results_part, self._path)

    def run_temps(self):
        print(f"\n{' Simulate Temperatures ':*^40}\n")

        tk_ref = self._params.gas['tk']
        tk_min = self._params.case['tk'][0]
        tk_max = self._params.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        # Store Umf at each temperature from Ergun and WenYu
        umf_ergun = []
        umf_wenyu = []

        # Store Ut at each temperature from Ganser and Haider
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
            gas = Gas(self._params.gas)
            gas.update_temperature(tk)

            # BFB model for fluidization
            bfb = BfbModel(gas, self._params)
            umf = bfb.calc_umf()
            ut_bed = bfb.calc_ut_bed()
            ut_bio = bfb.calc_ut_biomass()
            ut_char = bfb.calc_ut_char()

            # Pyrolysis model for biomass pyrolysis
            pyro = PyrolysisModel(gas, self._params)
            t_devol = pyro.calc_devol_time()

            # Append results for each temperature
            umf_ergun.append(umf.ergun)
            umf_wenyu.append(umf.wenyu)
            ut_bed_ganser.append(ut_bed.ganser)
            ut_bed_haider.append(ut_bed.haider)
            ut_bio_ganser.append(ut_bio.ganser)
            ut_bio_haider.append(ut_bio.haider)
            ut_char_ganser.append(ut_char.ganser)
            ut_char_haider.append(ut_char.haider)
            ts_devol.append(t_devol)

        uts_ganser = {'bed': ut_bed_ganser, 'bio': ut_bio_ganser, 'char': ut_char_ganser}
        uts_haider = {'bed': ut_bed_haider, 'bio': ut_bio_haider, 'char': ut_char_haider}

        plot_umf_temps(tks, umf_ergun, umf_wenyu, tk_ref, self._path)
        plot_ut_temps(tks, uts_ganser, uts_haider, self._path)
        plot_tdevol_temps(tks, ts_devol, tk_ref, self._path)

        print(f'Matplotlib figures saved to the `{self._path.name}` folder.\n')
