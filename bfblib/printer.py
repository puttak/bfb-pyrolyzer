import textwrap


def print_parameters(params):
    """
    Print parameters defined in the parameters module.
    """
    sp = ', '.join(params.gas['sp'])
    x = ', '.join([str(gx) for gx in params.gas['x']])
    w = 12  # width specifier

    pm_string = f"""
    {' Bed Particle ':-^40}\n
    {'dp':<{w}} {params.bed['dp']:<{w}} Mean particle diameter [m]
    {'dp_min':<{w}} {params.bed['dp_min']:<{w}} Minimum particle diameter [m]
    {'dp_max':<{w}} {params.bed['dp_max']:<{w}} Maximum particle diameter [m]
    {'phi':<{w}} {params.bed['phi']:<{w}} Sphericity [-]
    {'rho':<{w}} {params.bed['rho']:<{w}} Density [kg/m³]

    {' Biomass Particle ':-^40}\n
    {'dp':<{w}} {params.biomass['dp']:<{w}} Mean particle diameter [m]
    {'phi':<{w}} {params.biomass['phi']:<{w}} Particle sphericity [-]
    {'rho':<{w}} {params.biomass['rho']:<{w}} Density of loblolly pine [kg/m³]
    {'b':<{w}} {params.biomass['b']:<{w}} Shape factor for particle transient heat conduction[-]
    {'h':<{w}} {params.biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
    {'k':<{w}} {params.biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
    {'m':<{w}} {params.biomass['m']:<{w}} Number of nodes from particle center (m=0) to surface (m)
    {'mc':<{w}} {params.biomass['mc']:<{w}} Moisture content [%]
    {'nt':<{w}} {params.biomass['nt']:<{w}} Number of time steps for particle temperature profile [-]
    {'tki':<{w}} {params.biomass['tk_init']:<{w}} Initial particle temperature [K]
    {'t_max':<{w}} {params.biomass['t_max']:<{w}} Time duration to calculate particle temperature profile [s]

    {' Char Particle ':-^40}\n
    {'dp':<{w}} {params.char['dp']:<{w}} Mean particle diameter [m]
    {'phi':<{w}} {params.char['phi']:<{w}} Sphericity [-]
    {'rho':<{w}} {params.char['rho']:<{w}} Density [kg/m³]

    {' Gas Properties ':-^40}\n
    {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
    {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]
    {'p':<{w}} {params.gas['p']:<{w},} Gas pressure in reactor [Pa]
    {'tk':<{w}} {params.gas['tk']:<{w}} Gas temperature in reactor [K]

    {' Reactor Geometry and Conditions ':-^40}\n
    {'di':<{w}} {params.reactor['di']:<{w}} Inner diameter of reactor [m]
    {'ep':<{w}} {params.reactor['ep']:<{w}} Void fraction of bed [-]
    {'ht':<{w}} {params.reactor['ht']:<{w}} Total height of reactor [m]
    {'q':<{w}} {params.reactor['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
    {'zmf':<{w}} {params.reactor['zmf']:<{w}} Bed height at minimum fluidization [m]
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
    {'rho':<{w}} {gas.rho:<{w}.4f} Density [kg/m³]"""
    print(textwrap.dedent(gas_string))


def print_particle_results(bed, bio, char):
    """
    Print bed particle results from Particle class object.
    """
    w = 12  # width specifier

    particle_string = f"""
    {' Bed Particle ':-^40}\n
    {'umf_ergun':<{w}} {bed.umf_ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {bed.umf_wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {bed.ut_ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {bed.ut_haider:<{w}.2f} Terminal velocity [m/s]

    {' Biomass Particle ':-^40}\n
    {'t_devol':<{w}} {bio.t_devol:<{w}.2f} Devolatilization time for 95% conversion [s]
    {'t_ref':<{w}} {bio.t_ref:<{w}.2f} Time for particle center to reach T∞ [s]
    {'umf_ergun':<{w}} {bio.umf_ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {bio.umf_wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {bio.ut_ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {bio.ut_haider:<{w}.2f} Terminal velocity [m/s]

    {' Char Particle ':-^40}\n
    {'umf_ergun':<{w}} {char.umf_ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {char.umf_wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {char.ut_ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {char.ut_haider:<{w}.2f} Terminal velocity [m/s]"""
    print(textwrap.dedent(particle_string))


def print_bfb_results(bfb):
    """
    Print BFB model results.
    """
    w = 12  # width specifier

    bfb_string = f"""
    {' BFB Model ':-^40}\n
    {'ac':<{w}} {bfb.ac:<{w}.4f} Inner cross section area [m²]
    {'us':<{w}} {bfb.us:<{w}.4f} Superficial gas velocity [m/s]
    {'tdh_chan':<{w}} {bfb.tdh_chan:<{w}.4f} Transport disengaging height [m]
    {'tdh_horio':<{w}} {bfb.tdh_horio:<{w}.4f} Transport disengaging height [m]
    {'us_umf_ergun':<{w}} {bfb.us_umf_ergun:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'us_umf_wenyu':<{w}} {bfb.us_umf_wenyu:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp_ergun':<{w}} {bfb.zexp_ergun:<{w}.2f} Height of expanded bed [m]
    {'zexp_wenyu':<{w}} {bfb.zexp_wenyu:<{w}.2f} Height of expanded bed [m]"""
    print(textwrap.dedent(bfb_string))
