from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


def solve_temperatures(params):
    """
    Calculate results for gas, bed particle, biomass particle, and BFB reactor
    for a range of temperatures.

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

    # Range of temperatures for calculations
    tk = pm.gas['tk']
    tk_min = pm.gas['tk_min']
    tk_max = pm.gas['tk_max']
    tks = [tk_min, tk, tk_max]

    # Calculations
    bed = Particle.from_params(pm.bed)
    bio = Particle.from_params(pm.biomass)
    bfb = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])

    ep = pm.reactor['ep']
    tv_list = []
    tv_min_list = []
    tv_max_list = []
    umb_list = []
    umb_umf_list = []
    umf_ergun_list = []
    umf_wenyu_list = []
    us_list = []
    us_umf_ergun_list = []
    us_umf_wenyu_list = []
    ut_bed_ganser_list = []
    ut_bed_haider_list = []
    ut_bio_ganser_list = []
    ut_bio_haider_list = []

    for tk in tks:
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)

        tv, tv_min, tv_max = bio.calc_devol_time(tk)
        umb = bed.calc_umb(gas)
        umb_umf = bed.calc_umb_umf(gas)
        umf_ergun = bed.calc_umf_ergun(ep, gas)
        umf_wenyu = bed.calc_umf_wenyu(gas)
        us = bfb.calc_us(gas)
        us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
        us_umf_wenyu = bfb.calc_us_umf(us, umf_wenyu)
        ut_bed_ganser = bed.calc_ut_ganser(gas)
        ut_bed_haider = bed.calc_ut_haider(gas)
        ut_bio_ganser = bio.calc_ut_ganser(gas)
        ut_bio_haider = bio.calc_ut_haider(gas)

        tv_list.append(tv)
        tv_min_list.append(tv_min)
        tv_max_list.append(tv_max)
        umb_list.append(umb)
        umb_umf_list.append(umb_umf)
        umf_ergun_list.append(umf_ergun)
        umf_wenyu_list.append(umf_wenyu)
        us_list.append(us)
        us_umf_ergun_list.append(us_umf_ergun)
        us_umf_wenyu_list.append(us_umf_wenyu)
        ut_bed_ganser_list.append(ut_bed_ganser)
        ut_bed_haider_list.append(ut_bed_haider)
        ut_bio_ganser_list.append(ut_bio_ganser)
        ut_bio_haider_list.append(ut_bio_haider)

    # Store results
    results = {}
    results['tks'] = tks
    results['tv'] = tv_list
    results['tv_min'] = tv_min_list
    results['tv_max'] = tv_max_list
    results['umb'] = umb_list
    results['umb_umf'] = umb_umf_list
    results['umf_ergun'] = umf_ergun_list
    results['umf_wenyu'] = umf_wenyu_list
    results['us'] = us_list
    results['us_umf_ergun'] = us_umf_ergun_list
    results['us_umf_wenyu'] = us_umf_wenyu_list
    results['ut_bed_ganser'] = ut_bed_ganser_list
    results['ut_bed_haider'] = ut_bed_haider_list
    results['ut_bio_ganser'] = ut_bio_ganser_list
    results['ut_bio_haider'] = ut_bio_haider_list

    return results
