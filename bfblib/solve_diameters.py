import numpy as np

from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


def solve_diameters(params):
    """
    Calculate results for gas, bed particle, biomass particle, and BFB reactor
    for a range of particle diameters.

    Parameters
    ----------
    params : module
        Parameters from module file.

    Returns
    -------
    results : dict
        Results from calculations.
    """

    pm = params

    # Range of particle diameters for calculations
    dpmin = 0.00001
    dpmax = 0.001
    dps = np.linspace(dpmin, dpmax)

    # Calculations
    gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])
    bed = Particle.from_params(pm.bed)
    bio = Particle.from_params(pm.biomass)
    bfb = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])

    ep = pm.reactor['ep']
    us = bfb.calc_us(gas)

    umf_ergun = []
    umf_wenyu = []
    ut_bed_ganser = []
    ut_bed_haider = []
    ut_bio_ganser = []
    ut_bio_haider = []

    for dp in dps:
        bed.dp = dp
        bio.dp = dp

        umfergun = bed.calc_umf_ergun(ep, gas)
        umfwenyu = bed.calc_umf_wenyu(gas)
        utbed_ganser = bed.calc_ut_ganser(gas)
        utbed_haider = bed.calc_ut_haider(gas)
        utbio_ganser = bio.calc_ut_ganser(gas)
        utbio_haider = bio.calc_ut_haider(gas)

        umf_ergun.append(umfergun)
        umf_wenyu.append(umfwenyu)
        ut_bed_ganser.append(utbed_ganser)
        ut_bed_haider.append(utbed_haider)
        ut_bio_ganser.append(utbio_ganser)
        ut_bio_haider.append(utbio_haider)

    # Store results
    results = {}
    results['dps'] = dps
    results['us'] = us
    results['umf_ergun'] = umf_ergun
    results['umf_wenyu'] = umf_wenyu
    results['ut_bed_ganser'] = ut_bed_ganser
    results['ut_bed_haider'] = ut_bed_haider
    results['ut_bio_ganser'] = ut_bio_ganser
    results['ut_bio_haider'] = ut_bio_haider

    return results
