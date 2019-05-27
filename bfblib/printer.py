import textwrap


def print_parameters(pm):
    """
    here
    """
    pm_string = f"""
    === Reactor Parameters ===
    {'di':12} {pm.di} \t Inner diameter of reactor [m]

    === Gas Parameters ===
    {'gas':12} {', '.join(pm.gas)} \t Components of gas mixture
    {'p_gas':12} {pm.p_gas:,} \t Gas pressure in reactor [Pa]
    {'q_gas':12} {pm.q_gas} \t Volumetric flowrate of gas into reactor [SLM]
    {'t_gas':12} {pm.t_gas} \t Gas temperature in reactor [K]
    {'x_gas':12} {', '.join([str(x) for x in pm.x_gas])}  Mole fractions of gas mixture [-]

    === Bed Parameters ===
    {'dp':12} {pm.dp} \t Mean particle diameter [m]
    {'ep':12} {pm.ep} \t Void fraction of bed [-]
    {'phi':12} {pm.phi} \t Particle sphericity [-]
    {'rhos':12} {pm.rhos} \t Density of a bed particle [kg/m³]
    {'zmf':12} {pm.zmf} \t Bed height at minimum fluidization [m]
    """
    print(textwrap.dedent(pm_string))


def print_reactor(rct):
    """
    here
    """
    rct_string = f"""
    === Reactor Calculations ===
    {'a_inner':12} {rct.a_inner:.4f} \t Inner cross section area [m²]
    """
    print(textwrap.dedent(rct_string))


def print_gas(g):
    """
    here
    """
    g_string = f"""
    === Gas Properties for {g.formula} ===
    {'mw':12} {g.mw} \t Molecular weight [g/mol]
    {'mu':12} {g.mu:.2f} \t Viscosity [µP]
    {'rho':12} {g.rho:.4f} \t Density [kg/m³]
    {'us':12} {g.us:.4f} \t Superficial gas velocity [m/s]
    """
    print(textwrap.dedent(g_string))


def print_gas_mix(gm):
    """
    here
    """
    gm_string = f"""
    === Gas Mixture Properties ===
    {'mu_graham':12} {gm.mu_graham:.2f} \t Viscosity [µP]
    {'mu_herning':12} {gm.mu_herning:.2f} \t Viscosity [µP]
    {'mw':12} {gm.mw:.2f} \t Molecular weight of gas mixture [g/mol]
    {'rho':12} {gm.rho:.4f} \t Density of gas mixture [kg/m³]
    """
    print(textwrap.dedent(gm_string))


def print_bed_calcs(umf, us, zexp):
    """
    here
    """
    bp_string = f"""
    === Bed Calculations ===
    {'umf':12} {umf:.4f} \t Minimum fluidization velocity [m/s]
    {'us_umf':12} {us / umf:.2f} \t Us/Umf for gas and bed particles [-]
    {'zexp':12} {zexp:.2f} \t Height of expanded bed [m]
    """
    print(textwrap.dedent(bp_string))
