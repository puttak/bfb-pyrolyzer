import numpy as np

from .gas import Gas
from .particle import Particle
from .bfb_model import BfbModel

from .printer import print_parameters
from .printer import print_gas_properties
from .printer import print_particle_results
from .printer import print_bfb_results

from .plotter import plot_geldart
from .plotter import plot_intra_particle_heat_cond
from .plotter import plot_umf_temps
from .plotter import plot_tdevol_temps
from .plotter import plot_ut_temps


def run_params(params, path=None):

    # Gas properties
    # Note that gas mixture uses the Herning calculation for viscosity
    gas = Gas(params.gas['sp'], params.gas['x'], params.gas['p'], params.gas['tk'])

    # Bed particle
    dp = params.bed['dp']
    phi = params.bed['phi']
    rho = params.bed['rho']
    ep = params.reactor['ep']
    bed = Particle(dp, phi, rho)
    bed.calc_umf(ep, gas.mu, gas.rho)
    bed.calc_ut(gas.mu, gas.rho)

    # Biomass particle
    dp = params.biomass['dp']
    phi = params.biomass['phi']
    rho = params.biomass['sg'] * 1000
    b = params.biomass['b']
    h = params.biomass['h']
    k = params.biomass['k']
    m = params.biomass['m']
    mc = params.biomass['mc']
    nt = params.biomass['nt']
    tki = params.biomass['tki']
    t_max = params.biomass['t_max']
    bio = Particle(dp, phi, rho)
    bio.calc_umf(ep, gas.mu, gas.rho)
    bio.calc_ut(gas.mu, gas.rho)
    bio.build_time_vector(nt, t_max)
    bio.calc_trans_hc(b, h, k, m, mc, tki, gas.tk)
    bio.calc_time_tkinf(gas.tk)
    bio.calc_devol_time(gas.tk)

    # Char particle
    dp = params.char['dp']
    phi = params.char['phi']
    rho = params.char['rho']
    char = Particle(dp, phi, rho)
    char.calc_umf(ep, gas.mu, gas.rho)
    char.calc_ut(gas.mu, gas.rho)

    # BFB reactor model
    di = params.reactor['di']
    q = params.reactor['q']
    zmf = params.reactor['zmf']
    bfb = BfbModel(di, q, zmf)
    bfb.calc_us(gas)
    bfb.calc_us_umf(bed)
    bfb.calc_tdh()
    bfb.calc_zexp(bed, gas)

    # Print parameters to screen
    print(f"\n{' Parameters ':*^40}")
    print_parameters(params)

    # Print results to screen
    print(f"{' Results from Parameters ':*^40}")
    print_gas_properties(gas)
    print_particle_results(bed, bio, char)
    print_bfb_results(bfb)

    # Create and save plot figures if path is defined
    if path is not None:
        plot_geldart(gas, params, path)
        plot_intra_particle_heat_cond(bio, path)


def run_temps(params, path):
    print(f"\n{' Simulate Temperatures ':*^40}\n")

    tk_ref = params.gas['tk']
    tk_min = params.case['tk'][0]
    tk_max = params.case['tk'][1]
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

    # Bed particle
    dp_bed = params.bed['dp']
    phi_bed = params.bed['phi']
    rho_bed = params.bed['rho']
    bed = Particle(dp_bed, phi_bed, rho_bed)

    # Biomass particle
    dp_bio = params.biomass['dp']
    phi_bio = params.biomass['phi']
    rho_bio = params.biomass['sg'] * 1000
    bio = Particle(dp_bio, phi_bio, rho_bio)

    # Char particle
    dp_char = params.char['dp']
    phi_char = params.char['phi']
    rho_char = params.char['rho']
    char = Particle(dp_char, phi_char, rho_char)

    # BFB reactor parameters
    ep = params.reactor['ep']

    for tk in tks:
        print(f'Run case at {tk} K ...')

        # Gas properties at temperature
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(params.gas['sp'], params.gas['x'], params.gas['p'], tk)

        # Bed particle calculations
        bed.calc_umf(ep, gas.mu, gas.rho)
        bed.calc_ut(gas.mu, gas.rho)

        # Biomass particle calculations
        bio.calc_ut(gas.mu, gas.rho)
        bio.calc_devol_time(gas.tk)

        # Char particle calculations
        char.calc_ut(gas.mu, gas.rho)

        # Append results for each temperature
        umf_ergun.append(bed.umf_ergun)
        umf_wenyu.append(bed.umf_wenyu)
        ut_bed_ganser.append(bed.ut_ganser)
        ut_bed_haider.append(bed.ut_haider)
        ut_bio_ganser.append(bio.ut_ganser)
        ut_bio_haider.append(bio.ut_haider)
        ut_char_ganser.append(char.ut_ganser)
        ut_char_haider.append(char.ut_haider)
        ts_devol.append(bio.t_devol)

    uts_ganser = {'bed': ut_bed_ganser, 'bio': ut_bio_ganser, 'char': ut_char_ganser}
    uts_haider = {'bed': ut_bed_haider, 'bio': ut_bio_haider, 'char': ut_char_haider}

    plot_umf_temps(tks, umf_ergun, umf_wenyu, tk_ref, path)
    plot_ut_temps(tks, uts_ganser, uts_haider, path)
    plot_tdevol_temps(tks, ts_devol, tk_ref, path)

    print(f'Matplotlib figures saved to the `{path.name}` folder.\n')
