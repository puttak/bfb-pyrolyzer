import numpy as np

from .gas import Gas
from .particle import Particle
from .bfb_model import BfbModel

from .printer import print_params
from .printer import print_params_results

from .plotter import plot_geldart
from .plotter import plot_intra_particle_heat_cond
from .plotter import plot_umf_temps
from .plotter import plot_tdevol_temps
from .plotter import plot_ut_temps


def run_params(pm, path=None):

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

    # Print parameters and results to screen
    print_params(pm)
    print_params_results(bed, bfb, bio, char, gas)

    # Create and save plot figures if path is defined
    if path is not None:
        plot_geldart(gas, pm, path)
        plot_intra_particle_heat_cond(bio, path)


def run_temps(pm, path):
    print_params(pm)
    print(f"{'*':*^40}")
    print(f"{'Simulate Temperatures':^40}")
    print(f"{'*':*^40}\n")

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
        print(f'Run case at {tk} K ...')

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
    plot_umf_temps(tks, umf, tk_ref, path)
    plot_ut_temps(tks, ut_bed, ut_bio, ut_char, path)
    plot_tdevol_temps(tks, ts_devol, tk_ref, path)

    print(f'Matplotlib figures saved to the `{path.name}` folder.\n')
