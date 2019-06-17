import textwrap


def print_header(title):
    """
    Print header title for parameters or results.
    """
    print(f'\n>>>>>>>>>>>> {title} <<<<<<<<<<<<\n')


def print_parameters(params):
    """
    Print parameters defined in the parameters module.
    """
    sp = ', '.join(params.gas['sp'])
    x = ', '.join([str(gx) for gx in params.gas['x']])
    w = 12  # width specifier

    pm_string = f"""
    ------------- Bed --------------\n
    {'dp_mean':<{w}} {params.bed['dp'][0]:<{w}} Mean particle diameter [m]
    {'dp_min':<{w}} {params.bed['dp'][1]:<{w}} Minimum particle diameter [m]
    {'dp_max':<{w}} {params.bed['dp'][2]:<{w}} Maximum particle diameter [m]
    {'ep':<{w}} {params.bed['ep']:<{w}} Void fraction of bed [-]
    {'phi':<{w}} {params.bed['phi']:<{w}} Particle sphericity [-]
    {'rhos':<{w}} {params.bed['rhos']:<{w}} Density of a bed particle [kg/m³]
    {'zmf':<{w}} {params.bed['zmf']:<{w}} Bed height at minimum fluidization [m]

    ----------- Biomass ------------\n
    {'dp_mean':<{w}} {params.biomass['dp_mean']:<{w}} Mean particle diameter [m]
    {'h':<{w}} {params.biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
    {'k':<{w}} {params.biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
    {'mc':<{w}} {params.biomass['mc']:<{w}} Moisture content [%]
    {'sg':<{w}} {params.biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
    {'tk_i':<{w}} {params.biomass['tk_i']:<{w}} Initial particle temperature [K]

    ------------- Gas --------------\n
    {'p':<{w}} {params.gas['p']:<{w},} Gas pressure in reactor [Pa]
    {'q':<{w}} {params.gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
    {'sp':<{w}} {sp:<{w}} Comionents of gas mixture [-]
    {'tk':<{w}} {params.gas['tk']:<{w}} Gas temperature in reactor [K]
    {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

    ------------ Reactor -----------\n
    {'di':<{w}} {params.reactor['di']:<{w}} Inner diameter of reactor [m]
    """
    print(textwrap.dedent(pm_string))


def print_gas_properties(gas):
    """
    Print gas properties from a Gas class object.
    """
    w = 12  # width specifier

    gas_string = f"""
    -------- Gas Properties --------\n
    {'mw':<{w}} {gas.mw:<{w}.4f} Molecular weight [g/mol]
    {'mu':<{w}} {gas.mu:<{w}.2f} Viscosity [µP]
    {'rho':<{w}} {gas.rho:<{w}.4f} Density [kg/m³]
    """
    print(textwrap.dedent(gas_string))


def print_bfb_results(bfb):
    """
    Print BFB model results.
    """
    w = 12  # width specifier

    bfb_string = f"""
    ----------- BFB Model ----------\n
    {'ac':<{w}} {bfb.ac:<{w}.4f} Inner cross section area [m²]
    {'us':<{w}} {bfb.us:<{w}.4f} Superficial gas velocity [m/s]

    Ergun
    {'umf':<{w}} {bfb.umf_ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {bfb.us_umf_ergun:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {bfb.zexp_ergun:<{w}.2f} Height of expanded bed [m]

    Wen and Yu
    {'umf':<{w}} {bfb.umf_wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'us_umf':<{w}} {bfb.us_umf_wenyu:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp':<{w}} {bfb.zexp_wenyu:<{w}.2f} Height of expanded bed [m]
    """
    print(textwrap.dedent(bfb_string))


def print_particle_results(particle):
    """
    Print particle model results.
    """
    w = 12  # width specifier

    particle_string = f"""
    -------- Particle Model --------\n
    {'t_tkinf':<{w}} {particle.t_tkinf:<{w}.2f} Time for particle center to reach T∞ [s]
    """
    print(textwrap.dedent(particle_string))


def print_pyrolysis_results(pyrolysis):
    """
    Print pyrolysis model results.
    """
    w = 12  # width specifier

    res_string = f"""
    -------- Pyrolysis Model -------\n
    {'t_devol':<{w}} {pyrolysis.t_devol:<{w}.2f} Devolatilization time for 95% conversion [s]
    """
    print(textwrap.dedent(res_string))
