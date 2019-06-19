import textwrap


def print_parameters(params):
    """
    Print parameters defined in the parameters module.
    """
    sp = ', '.join(params.gas['sp'])
    x = ', '.join([str(gx) for gx in params.gas['x']])
    w = 12  # width specifier

    pm_string = f"""
    {' Bed ':-^40}\n
    {'dp_mean':<{w}} {params.bed['dp'][0]:<{w}} Mean particle diameter [m]
    {'dp_min':<{w}} {params.bed['dp'][1]:<{w}} Minimum particle diameter [m]
    {'dp_max':<{w}} {params.bed['dp'][2]:<{w}} Maximum particle diameter [m]
    {'ep':<{w}} {params.bed['ep']:<{w}} Void fraction of bed [-]
    {'phi':<{w}} {params.bed['phi']:<{w}} Particle sphericity [-]
    {'rhos':<{w}} {params.bed['rhos']:<{w}} Density of a bed particle [kg/m³]
    {'zmf':<{w}} {params.bed['zmf']:<{w}} Bed height at minimum fluidization [m]

    {' Biomass ':-^40}\n
    {'dp_mean':<{w}} {params.biomass['dp_mean']:<{w}} Mean particle diameter [m]
    {'h':<{w}} {params.biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
    {'k':<{w}} {params.biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
    {'mc':<{w}} {params.biomass['mc']:<{w}} Moisture content [%]
    {'sg':<{w}} {params.biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
    {'tk_i':<{w}} {params.biomass['tk_i']:<{w}} Initial particle temperature [K]

    {' Gas ':-^40}\n
    {'p':<{w}} {params.gas['p']:<{w},} Gas pressure in reactor [Pa]
    {'q':<{w}} {params.gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
    {'sp':<{w}} {sp:<{w}} Comionents of gas mixture [-]
    {'tk':<{w}} {params.gas['tk']:<{w}} Gas temperature in reactor [K]
    {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

    {' Reactor ':-^40}\n
    {'di':<{w}} {params.reactor['di']:<{w}} Inner diameter of reactor [m]
    {'ht':<{w}} {params.reactor['ht']:<{w}} Total height of reactor [m]
    """
    print(textwrap.dedent(pm_string))


def print_gas_properties(gas):
    """
    Print gas properties from a Gas class object.
    """
    w = 12  # width specifier

    gas_string = f"""
    {' Gas Properties ':-^40}\n
    {'mw':<{w}} {gas.mw:<{w}.4f} Molecular weight [g/mol]
    {'mu':<{w}} {gas.mu:<{w}.2f} Viscosity [µP]
    {'rho':<{w}} {gas.rho:<{w}.4f} Density [kg/m³]
    """
    print(textwrap.dedent(gas_string))


def print_bfb_results(results):
    """
    Print BFB model results.
    """
    ac, us, tdh, umf, us_umf, zexp, ut_bed, ut_bio, ut_char = results
    w = 12  # width specifier

    bfb_string = f"""
    {' BFB Model ':-^40}\n
    {'ac':<{w}} {ac:<{w}.4f} Inner cross section area [m²]
    {'us':<{w}} {us:<{w}.4f} Superficial gas velocity [m/s]
    {'tdh_chan':<{w}} {tdh.chan:<{w}.4f} Transport disengaging Height [m]
    {'tdh_horio':<{w}} {tdh.horio:<{w}.4f} Transport disengaging Height [m]

    Ergun
    {'umf':<{w}} {umf.ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {us_umf.ergun:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {zexp.ergun:<{w}.2f} Height of expanded bed [m]

    Wen and Yu
    {'umf':<{w}} {umf.wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {us_umf.wenyu:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {zexp.wenyu:<{w}.2f} Height of expanded bed [m]

    Bed material
    {'ut_ganser':<{w}} {ut_bed.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {ut_bed.haider:<{w}.2f} Terminal velocity [m/s]

    Biomass material
    {'ut_ganser':<{w}} {ut_bio.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {ut_bio.haider:<{w}.2f} Terminal velocity [m/s]

    Char material
    {'ut_ganser':<{w}} {ut_char.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {ut_char.haider:<{w}.2f} Terminal velocity [m/s]
    """
    print(textwrap.dedent(bfb_string))


def print_particle_results(results):
    """
    Print particle model results.
    """
    t_hc, tk_hc, t_tkinf = results
    w = 12  # width specifier

    particle_string = f"""
    {' Particle Model ':-^40}\n
    {'t_tkinf':<{w}} {t_tkinf:<{w}.2f} Time for particle center to reach T∞ [s]
    """
    print(textwrap.dedent(particle_string))


def print_pyrolysis_results(results):
    """
    Print pyrolysis model results.
    """
    t_devol, = results
    w = 12  # width specifier

    res_string = f"""
    {' Pyrolysis Model ':-^40}\n
    {'t_devol':<{w}} {t_devol:<{w}.2f} Devolatilization time for 95% conversion [s]
    """
    print(textwrap.dedent(res_string))
