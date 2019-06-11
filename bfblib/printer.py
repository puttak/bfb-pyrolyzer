import textwrap


def print_parameters(pm):
    """
    Print parameter names, values, and descriptions to terminal.
    """
    bed = pm.bed
    biomass = pm.biomass
    gas = pm.gas
    reactor = pm.reactor

    if type(pm.gas['sp']) is list:
        sp = ', '.join(pm.gas['sp'])
        x = ', '.join([str(gx) for gx in pm.gas['x']])
    else:
        sp = pm.gas['sp']
        x = pm.gas['x']

    w = 12  # width specifier

    pm_string = f"""
    <<<<<<<<<< Parameters >>>>>>>>>>

    ------------- Bed --------------\n
    {'dp_mean':<{w}} {bed['dps'][0]:<{w}} Mean particle diameter [m]
    {'dp_min':<{w}} {bed['dps'][1]:<{w}} Minimum particle diameter [m]
    {'dp_max':<{w}} {bed['dps'][2]:<{w}} Maximum particle diameter [m]
    {'ep':<{w}} {bed['ep']:<{w}} Void fraction of bed [-]
    {'phi':<{w}} {bed['phi']:<{w}} Particle sphericity [-]
    {'rhos':<{w}} {bed['rhos']:<{w}} Density of a bed particle [kg/m³]
    {'zmf':<{w}} {bed['zmf']:<{w}} Bed height at minimum fluidization [m]

    ----------- Biomass ------------\n
    {'dp_mean':<{w}} {biomass['dp_mean']:<{w}} Mean particle diameter [m]
    {'h':<{w}} {biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
    {'k':<{w}} {biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
    {'mc':<{w}} {biomass['mc']:<{w}} Moisture content [%]
    {'sg':<{w}} {biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
    {'ti':<{w}} {biomass['ti']:<{w}} Initial particle temperature [K]

    ------------- Gas --------------\n
    {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
    {'p':<{w}} {gas['p']:<{w},} Gas pressure in reactor [Pa]
    {'q':<{w}} {gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
    {'tk':<{w}} {gas['tk']:<{w}} Gas temperature in reactor [K]
    {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

    ------------ Reactor -----------\n
    {'di':<{w}} {reactor['di']:<{w}} Inner diameter of reactor [m]
    """
    print(textwrap.dedent(pm_string))


def print_bfb_results(results):
    """
    Print BFB model results to terminal.
    """
    w = 12  # width specifier

    res_string = f"""
    <<<<<<<<<<<< Results >>>>>>>>>>>>

    -------- Gas Properties --------\n
    {'mw':<{w}} {results['gas_mw']:<{w}.4f} Molecular weight [g/mol]
    {'mu':<{w}} {results['gas_mu']:<{w}.2f} Viscosity [µP]
    {'rho':<{w}} {results['gas_rho']:<{w}.4f} Density [kg/m³]

    ----------- BFB Model ----------\n
    {'ac':<{w}} {results['ac']:<{w}.4f} Inner cross section area [m²]
    {'us':<{w}} {results['us']:<{w}.4f} Superficial gas velocity [m/s]

    Ergun
    {'umf':<{w}} {results['umf_ergun']:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {results['us_umf_ergun']:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {results['zexp_ergun']:<{w}.2f} Height of expanded bed [m]

    Wen and Yu
    {'umf':<{w}} {results['umf_wenyu']:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {results['us_umf_wenyu']:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {results['zexp_wenyu']:<{w}.2f} Height of expanded bed [m]

    {'t_devol':<{w}} {results['t_devol']:<{w}.2f} Devolatilization time for 95% conversion [s]
    {'t_tkinf':<{w}} {results['t_tkinf']:<{w}.2f} Time for particle center to reach T∞ [s]
    """
    print(textwrap.dedent(res_string))
