import textwrap


def _params_string(pm):
    """
    Print parameters defined in the parameters module.
    """
    sp = ', '.join(pm.gas['sp'])
    x = ', '.join([str(gx) for gx in pm.gas['x']])
    w = 12  # width specifier

    pm_string = f"""
    {pm.case['case_system']}
    {pm.case['case_reactor']}
    Case {pm.case['case_num']} - {pm.case['case_desc']}

    {'*':*^40}
    {'Parameters':^40}
    {'*':*^40}

    {' Bed Particle ':-^40}\n
    {pm.bed['sample_desc']:<{w}}
    {pm.bed['sample_id']:<{w}}\n
    {'dp':<{w}} {pm.bed['dp']:<{w}} Mean particle diameter [m]
    {'dp_min':<{w}} {pm.bed['dp_min']:<{w}} Minimum particle diameter [m]
    {'dp_max':<{w}} {pm.bed['dp_max']:<{w}} Maximum particle diameter [m]
    {'phi':<{w}} {pm.bed['phi']:<{w}} Sphericity [-]
    {'rho':<{w}} {pm.bed['rho']:<{w}} Density [kg/m³]

    {' Biomass Particle ':-^40}\n
    {pm.biomass['sample_desc']:<{w}}
    {pm.biomass['sample_id']:<{w}}\n
    {'dp':<{w}} {pm.biomass['dp']:<{w}} Mean particle diameter [m]
    {'phi':<{w}} {pm.biomass['phi']:<{w}} Particle sphericity [-]
    {'rho':<{w}} {pm.biomass['rho']:<{w}} Density of loblolly pine [kg/m³]
    {'b':<{w}} {pm.biomass['b']:<{w}} Shape factor for particle transient heat conduction[-]
    {'h':<{w}} {pm.biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
    {'k':<{w}} {pm.biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
    {'m':<{w}} {pm.biomass['m']:<{w}} Number of nodes from particle center (m=0) to surface (m)
    {'mc':<{w}} {pm.biomass['mc']:<{w}} Moisture content [%]
    {'nt':<{w}} {pm.biomass['nt']:<{w}} Number of time steps for particle temperature profile [-]
    {'tki':<{w}} {pm.biomass['tk_init']:<{w}} Initial particle temperature [K]
    {'t_max':<{w}} {pm.biomass['t_max']:<{w}} Time duration to calculate particle temperature profile [s]

    {' Char Particle ':-^40}\n
    {'dp':<{w}} {pm.char['dp']:<{w}} Mean particle diameter [m]
    {'phi':<{w}} {pm.char['phi']:<{w}} Sphericity [-]
    {'rho':<{w}} {pm.char['rho']:<{w}} Density [kg/m³]

    {' Gas Properties ':-^40}\n
    {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
    {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]
    {'p':<{w}} {pm.gas['p']:<{w},} Gas pressure in reactor [Pa]
    {'tk':<{w}} {pm.gas['tk']:<{w}} Gas temperature in reactor [K]

    {' Reactor Geometry and Conditions ':-^40}\n
    {'di':<{w}} {pm.reactor['di']:<{w}} Inner diameter of reactor [m]
    {'ep':<{w}} {pm.reactor['ep']:<{w}} Void fraction of bed [-]
    {'ht':<{w}} {pm.reactor['ht']:<{w}} Total height of reactor [m]
    {'q':<{w}} {pm.reactor['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
    {'zmf':<{w}} {pm.reactor['zmf']:<{w}} Bed height at minimum fluidization [m]
    """
    return textwrap.dedent(pm_string)


def _results_string(bed, bfb, bio, char, gas):
    """
    Print results calculated from parameters module.
    """
    w = 12  # width specifier

    res_string = f"""
    {'*':*^40}
    {'Results':^40}
    {'*':*^40}

    {' Gas Properties ':-^40}\n
    {'mw':<{w}} {gas.mw:<{w}.4f} Molecular weight [g/mol]
    {'mu':<{w}} {gas.mu:<{w}.2f} Viscosity [µP]
    {'rho':<{w}} {gas.rho:<{w}.4f} Density [kg/m³]

    {' Bed Particle ':-^40}\n
    {'umf_ergun':<{w}} {bed.umf.ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {bed.umf.wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {bed.ut.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {bed.ut.haider:<{w}.2f} Terminal velocity [m/s]

    {' Biomass Particle ':-^40}\n
    {'t_devol':<{w}} {bio.t_devol:<{w}.2f} Devolatilization time for 95% conversion [s]
    {'t_ref':<{w}} {bio.t_ref:<{w}.2f} Time for particle center to reach T∞ [s]
    {'umf_ergun':<{w}} {bio.umf.ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {bio.umf.wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {bio.ut.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {bio.ut.haider:<{w}.2f} Terminal velocity [m/s]

    {' Char Particle ':-^40}\n
    {'umf_ergun':<{w}} {char.umf.ergun:<{w}.4f} Minimum fluidization velocity [m/s]
    {'umf_wenyu':<{w}} {char.umf.wenyu:<{w}.4f} Minimum fluidization velocity [m/s]
    {'ut_ganser':<{w}} {char.ut.ganser:<{w}.2f} Terminal velocity [m/s]
    {'ut_haider':<{w}} {char.ut.haider:<{w}.2f} Terminal velocity [m/s]

    {' BFB Model ':-^40}\n
    {'ac':<{w}} {bfb.ac:<{w}.4f} Inner cross section area [m²]
    {'us':<{w}} {bfb.us:<{w}.4f} Superficial gas velocity [m/s]
    {'tdh_chan':<{w}} {bfb.tdh.chan:<{w}.4f} Transport disengaging height [m]
    {'tdh_horio':<{w}} {bfb.tdh.horio:<{w}.4f} Transport disengaging height [m]
    {'us_umf_ergun':<{w}} {bfb.us_umf.ergun:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'us_umf_wenyu':<{w}} {bfb.us_umf.wenyu:<{w}.2f} Us/Umf for gas and bed particles [-]
    {'zexp_ergun':<{w}} {bfb.zexp.ergun:<{w}.2f} Height of expanded bed [m]
    {'zexp_wenyu':<{w}} {bfb.zexp.wenyu:<{w}.2f} Height of expanded bed [m]
    """
    return textwrap.dedent(res_string)


def print_report(pm, bed, bfb, bio, char, gas, path):
    """
    Write parameters and results file for reporting purposes.
    """
    params_string = _params_string(pm)
    results_string = _results_string(bed, bfb, bio, char, gas)

    with open(path / 'report.txt', 'w') as f:
        print(params_string, file=f)
        print(results_string, file=f)
