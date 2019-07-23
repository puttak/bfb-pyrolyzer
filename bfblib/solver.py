import json
import logging
import numpy as np

from .gas import Gas
from .particle import Particle
from .bfb_model import BfbModel

from .plotter import plot_geldart
from .plotter import plot_intra_particle_heat_cond
from .printer import print_report
from .plotter import plot_umf_temps
from .plotter import plot_tdevol_temps
from .plotter import plot_ut_temps

from .helpers import results_params


class Solver:
    """
    Perform BFB calculations and save results to file.
    """

    def __init__(self, params, path):
        self.params = params
        self.path = path

    def solve_params(self):
        """
        """
        pm = self.params

        logging.info('Solve using parameters from Case %s', pm.case['case_num'])

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])

        # Bed particle
        bed = Particle.from_params(pm.bed)
        bed.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        bed.calc_ut(gas.mu, gas.rho)

        # Biomass particle
        bio = Particle.from_params(pm.biomass)
        bio.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        bio.calc_ut(gas.mu, gas.rho)
        bio.build_time_vector(pm.biomass['nt'], pm.biomass['t_max'])
        bio.calc_trans_hc(pm.biomass['b'], pm.biomass['h'], pm.biomass['k'], pm.biomass['m'], pm.biomass['mc'], pm.biomass['tk_init'], gas.tk)
        bio.calc_time_tkinf(gas.tk)
        bio.calc_devol_time(gas.tk)

        # Char particle
        char = Particle.from_params(pm.char)
        char.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        char.calc_ut(gas.mu, gas.rho)

        # BFB reactor model
        bfb = BfbModel(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
        bfb.calc_us(gas)
        bfb.calc_us_umf(bed)
        bfb.calc_tdh()
        bfb.calc_zexp(bed, gas)

        # Generate and save plots
        plot_geldart(gas, pm, self.path)
        plot_intra_particle_heat_cond(bio, self.path)

        # Print parameters and results to text file
        print_report(pm, bed, bfb, bio, char, gas, self.path)

        # Store results from parameters calculations
        self.results_params = results_params(pm, gas, bed, bio, char, bfb)

    def solve_temps(self):
        """
        """
        pm = self.params

        tk_min = pm.case['tk'][0]
        tk_max = pm.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        # Store Umf, Ut, and devolatilization time at each temperature
        umf = []
        ut_bed = []
        ut_bio = []
        ut_char = []
        ts_devol = []

        # Bed, biomass, and char particle
        bed = Particle.from_params(pm.bed)
        bio = Particle.from_params(pm.biomass)
        char = Particle.from_params(pm.char)

        # BFB reactor parameters
        ep = pm.reactor['ep']

        for tk in tks:
            # Gas properties at temperature
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)

            # Bed particle calculations
            bed.calc_umf(ep, gas.mu, gas.rho)
            bed.calc_ut(gas.mu, gas.rho)

            # Biomass particle calculations
            bio.calc_ut(gas.mu, gas.rho)
            bio.calc_devol_time(gas.tk)

            # Char particle calculations
            char.calc_ut(gas.mu, gas.rho)

            # Append results for each temperature
            umf.append(bed.umf)
            ut_bed.append(bed.ut)
            ut_bio.append(bio.ut)
            ut_char.append(char.ut)
            ts_devol.append(bio.t_devol)

        tk_ref = pm.gas['tk']
        plot_umf_temps(tks, umf, tk_ref, self.path)
        plot_ut_temps(tks, ut_bed, ut_bio, ut_char, self.path)
        plot_tdevol_temps(tks, ts_devol, tk_ref, self.path)

    def save_results(self):
        """
        """
        path = self.path
        results = self.results_params

        # Write results dictionary as JSON file to case directory
        with open(path / 'results.json', 'w') as fp:
            json.dump(results, fp, indent=4)
