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
    print(f"\n{' Simulate Temperatures ':*^40}\n")

    tk_ref = pm.gas['tk']
    tk_min = pm.case['tk'][0]
    tk_max = pm.case['tk'][1]
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
        umf_ergun.append(bed.umf.ergun)
        umf_wenyu.append(bed.umf.wenyu)
        ut_bed_ganser.append(bed.ut.ganser)
        ut_bed_haider.append(bed.ut.haider)
        ut_bio_ganser.append(bio.ut.ganser)
        ut_bio_haider.append(bio.ut.haider)
        ut_char_ganser.append(char.ut.ganser)
        ut_char_haider.append(char.ut.haider)
        ts_devol.append(bio.t_devol)

    uts_ganser = {'bed': ut_bed_ganser, 'bio': ut_bio_ganser, 'char': ut_char_ganser}
    uts_haider = {'bed': ut_bed_haider, 'bio': ut_bio_haider, 'char': ut_char_haider}

    plot_umf_temps(tks, umf_ergun, umf_wenyu, tk_ref, path)
    plot_ut_temps(tks, uts_ganser, uts_haider, path)
    plot_tdevol_temps(tks, ts_devol, tk_ref, path)

    print(f'Matplotlib figures saved to the `{path.name}` folder.\n')
