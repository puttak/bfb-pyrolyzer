import textwrap


def print_parameters(pm):
    """
    Print parameter names, values, and descriptions to console.
    """
    pm_string = f"""
    ========== Parameters ==========

    --- Bed ---\n
    {'dp':12} {pm.dp} \t Mean particle diameter [m]
    {'ep':12} {pm.ep} \t Void fraction of bed [-]
    {'phi':12} {pm.phi} \t Particle sphericity [-]
    {'rhos':12} {pm.rhos} \t Density of a bed particle [kg/m³]
    {'zmf':12} {pm.zmf} \t Bed height at minimum fluidization [m]

    --- Feedstock ---\n
    {'dp_feed':12} {pm.dp_feed} \t Mean particle diameter of biomass feedstock [m]

    --- Gas ---\n
    {'gas':12} {', '.join(pm.gas)} \t Components of gas mixture
    {'p_gas':12} {pm.p_gas:,} \t Gas pressure in reactor [Pa]
    {'q_gas':12} {pm.q_gas} \t Volumetric flowrate of gas into reactor [SLM]
    {'t_gas':12} {pm.t_gas} \t Gas temperature in reactor [K]
    {'x_gas':12} {', '.join([str(x) for x in pm.x_gas])}  Mole fractions of gas mixture [-]

    --- Reactor ---\n
    {'di':12} {pm.di} \t Inner diameter of reactor [m]
    """
    print(textwrap.dedent(pm_string))


def print_results(results):
    """
    Printe results to console.
    """
    a_inner = results['reactor'][0]

    mw_h2 = results['gas_h2'][0]
    mu_h2 = results['gas_h2'][1]
    rho_h2 = results['gas_h2'][2]
    us_h2 = results['gas_h2'][3]

    mw_n2 = results['gas_n2'][0]
    mu_n2 = results['gas_n2'][1]
    rho_n2 = results['gas_n2'][2]
    us_n2 = results['gas_n2'][3]

    mu_graham = results['gas_mix'][0]
    mu_herning = results['gas_mix'][1]
    mw_mix = results['gas_mix'][2]
    rho_mix = results['gas_mix'][3]

    umf = results['bed'][0]
    zexp = results['bed'][1]

    tv = results['feedstock'][0]

    res_string = f"""
    =========== Results ===========

    --- Reactor ---\n
    {'a_inner':12} {a_inner:.4f} \t Inner cross section area [m²]

    --- Gas H2 ---\n
    {'mw':12} {mw_h2} \t Molecular weight [g/mol]
    {'mu':12} {mu_h2:.2f} \t Viscosity [µP]
    {'rho':12} {rho_h2:.4f} \t Density [kg/m³]
    {'us':12} {us_h2:.4f} \t Superficial gas velocity [m/s]

    --- Gas N2 ---\n
    {'mw':12} {mw_n2} \t Molecular weight [g/mol]
    {'mu':12} {mu_n2:.2f} \t Viscosity [µP]
    {'rho':12} {rho_n2:.4f} \t Density [kg/m³]
    {'us':12} {us_n2:.4f} \t Superficial gas velocity [m/s]

    --- Gas Mixture of H2 and N2---\n
    {'mu_graham':12} {mu_graham:.2f} \t Viscosity [µP]
    {'mu_herning':12} {mu_herning:.2f} \t Viscosity [µP]
    {'mw':12} {mw_mix:.2f} \t Molecular weight of gas mixture [g/mol]
    {'rho':12} {rho_mix:.4f} \t Density of gas mixture [kg/m³]

    --- Bed ---\n
    {'umf':12} {umf:.4f} \t Minimum fluidization velocity [m/s]
    {'us_umf':12} {us_h2 / umf:.2f} \t Us/Umf for gas and bed particles [-]
    {'zexp':12} {zexp:.2f} \t Height of expanded bed [m]

    --- Feedstock ---\n
    {'tv':12} {tv:.2f} \t Devolatilization time for 95% conversion [s]
    """
    print(textwrap.dedent(res_string))
