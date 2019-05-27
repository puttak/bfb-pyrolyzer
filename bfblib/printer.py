import textwrap


def print_params(p):
    """
    here
    """

    p_string = f"""
    === Parameters ===
    {'di':12} {p.di} \t Inner diameter of reactor [m]
    {'dp':12} {p.dp} \t Mean particle diameter [m]
    """

    p_dedent = textwrap.dedent(p_string)
    print(p_dedent)


def print_gas(g):
    """
    here
    """
    g_string = f"""
    === Gas Properties {g.formula} ===
    {'press':12} {g.press:,} \t Pressure [Pa]
    {'temp':12} {g.temp} \t Temperature [K]
    {'x':12} {g.x} \t Mole fraction [-]
    {'mw':12} {g.mw} \t Molecular weight [g/mol]
    {'mu':12} {g.mu:.2f} \t Viscosity [µP]
    {'rho':12} {g.rho:.4f} \t Density [kg/m³]
    """

    g_dedent = textwrap.dedent(g_string)
    print(g_dedent)


def print_gas_mix(gm):
    """
    here
    """
    gm_string = f"""
    === Gas Mixture Properties ===
    {'mu_graham':12} {gm.mu_graham:.2f} \t Viscosity [µP]
    {'mu_herning':12} {gm.mu_herning:.2f} \t Viscosity [µP]
    {'mw':12} {gm.mw:.2f} \t Molecular weight [g/mol]
    """

    gm_dedent = textwrap.dedent(gm_string)
    print(gm_dedent)


def print_bed_particle(umf):
    """
    here
    """
    bp_string = f"""
    === Bed Particle Properties ===
    {'umf':12} {umf:.4f} \t Minimum fluidization velocity [m/s]
    """

    bp_dedent = textwrap.dedent(bp_string)
    print(bp_dedent)
