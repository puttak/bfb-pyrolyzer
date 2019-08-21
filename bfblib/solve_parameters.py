from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


def solve_parameters(params):
    """
    Calculate results for gas, bed particle, biomass particle, and BFB reactor.

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
    results = {}

    # Gas results
    gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])

    results['mw'] = gas.mw
    results['mug'] = gas.mu
    results['rhog'] = gas.rho

    # Bed particle results
    bed = Particle.from_params(pm.bed)

    umb = bed.calc_umb(gas)
    umb_umf = bed.calc_umb_umf(gas)
    umf_ergun = bed.calc_umf_ergun(pm.reactor['ep'], gas)
    umf_wenyu = bed.calc_umf_wenyu(gas)
    ut_bed_ganser = bed.calc_ut_ganser(gas)
    ut_bed_haider = bed.calc_ut_haider(gas)

    results['umb'] = umb
    results['umb_umf'] = umb_umf
    results['umf_ergun'] = umf_ergun
    results['umf_wenyu'] = umf_wenyu
    results['ut_bed_ganser'] = ut_bed_ganser
    results['ut_bed_haider'] = ut_bed_haider

    # Biomass particle results
    bio = Particle.from_params(pm.biomass)

    t_hc = bio.build_time_vector(pm.biomass['nt'], pm.biomass['t_max'])
    tk_hc = bio.calc_trans_hc(pm.biomass['b'], pm.biomass['h'], pm.biomass['k'], pm.biomass['m'], pm.biomass['mc'], t_hc, pm.biomass['tk_init'], gas.tk)
    t_ref = bio.calc_time_tkinf(t_hc, tk_hc, gas.tk)
    tv, tv_min, tv_max = bio.calc_devol_time(gas.tk)
    ut_bio_ganser = bio.calc_ut_ganser(gas)
    ut_bio_haider = bio.calc_ut_haider(gas)

    results['t_hc'] = t_hc
    results['tk_hc'] = tk_hc
    results['t_ref'] = t_ref
    results['tv'] = tv
    results['tv_min'] = tv_min
    results['tv_max'] = tv_max
    results['ut_bio_ganser'] = ut_bio_ganser
    results['ut_bio_haider'] = ut_bio_haider

    # BFB reactor results
    bfb = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])

    us = bfb.calc_us(gas)
    us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
    us_umf_wenyu = bfb.calc_us_umf(us, umf_wenyu)
    tdh_chan = bfb.calc_tdh_chan(us)
    tdh_horio = bfb.calc_tdh_horio(us)
    zexp_ergun = bfb.calc_zexp_ergun(bed, gas, umf_ergun, us)
    zexp_wenyu = bfb.calc_zexp_wenyu(bed, gas, umf_wenyu, us)

    results['ac'] = bfb.ac
    results['us'] = us
    results['us_umf_ergun'] = us_umf_ergun
    results['us_umf_wenyu'] = us_umf_wenyu
    results['tdh_chan'] = tdh_chan
    results['tdh_horio'] = tdh_horio
    results['zexp_ergun'] = zexp_ergun
    results['zexp_wenyu'] = zexp_wenyu

    return results
