import textwrap


def print_parameters(pm):
    """
    Print parameter names, values, and descriptions to terminal.
    """
    bed = pm.bed
    feed = pm.feed
    gas = pm.gas
    reactor = pm.reactor

    pm_string = f"""
    <<<<<<<<<< Parameters >>>>>>>>>>

    ------------- Bed --------------\n
    {'dp_mean':12} {bed['dps'][0]} \t Mean particle diameter [m]
    {'ep':12} {bed['ep']} \t Void fraction of bed [-]
    {'phi':12} {bed['phi']} \t Particle sphericity [-]
    {'rhos':12} {bed['rhos']} \t Density of a bed particle [kg/m³]
    {'zmf':12} {bed['zmf']} \t Bed height at minimum fluidization [m]

    ---------- Feedstock -----------\n
    {'dp_mean':12} {feed['dp_mean']} \t Mean particle diameter of biomass feedstock [m]

    ------------- Gas --------------\n
    {'sp':12} {', '.join(gas['sp'])} \t Components of gas mixture
    {'p':12} {gas['p']:,} \t Gas pressure in reactor [Pa]
    {'q':12} {gas['q']} \t Volumetric flowrate of gas into reactor [SLM]
    {'tk':12} {gas['tk']} \t Gas temperature in reactor [K]
    {'x':12} {', '.join([str(x) for x in gas['x']])}  Mole fractions of gas mixture [-]

    ------------ Reactor -----------\n
    {'di':12} {reactor['di']} \t Inner diameter of reactor [m]
    """
    print(textwrap.dedent(pm_string))


def print_gas_properties(gas):
    """
    Print gas properties to terminal.
    """
    res_string = f"""
    <<<<<<<<<<<< Results >>>>>>>>>>>>

    -------------- Gas -------------\n
    {'sp':12} {gas.sp} \t Gas species [-]
    {'mw':12} {gas.mw:.4f} \t Molecular weight [g/mol]
    {'mu':12} {gas.mu:.2f} \t Viscosity [µP]
    {'rho':12} {gas.rho:.4f} \t Density [kg/m³]"""
    print(textwrap.dedent(res_string))


def print_gas_mix_properties(gasmix):
    """
    Print gas mixture properties to terminal.
    """
    res_string = f"""
    <<<<<<<<<<<< Results >>>>>>>>>>>>

    ---------- Gas Mixture ---------\n
    {'sp':12} {gasmix.sp} \t Gas species [-]
    {'mw':12} {gasmix.mw:.4f} \t Molecular weight [g/mol]
    {'mu':12} {gasmix.mu_graham:.2f} \t Viscosity (Graham) [µP]
    {'mu':12} {gasmix.mu_herning:.2f} \t Viscosity (Herning) [µP]
    {'rho':12} {gasmix.rho:.4f} \t Density [kg/m³]"""
    print(textwrap.dedent(res_string))


def print_bfb_results(results):
    """
    Print BFB model results to terminal.
    """
    res_string = f"""
    ----------- BFB Model ----------\n
    {'ac':12} {results['ac']:.4f} \t Inner cross section area [m²]
    {'us':12} {results['us']:.4f} \t Superficial gas velocity [m/s]
    {'umf_ergun':12} {results['umf_ergun']:.4f} \t Minimum fluidization velocity [m/s]
    {'us_umf':12} {results['us_umf']:.2f} \t Us/Umf for gas and bed particles [-]
    {'zexp':12} {results['zexp']:.2f} \t Height of expanded bed [m]
    {'t_devol':12} {results['t_devol']:.2f} \t Devolatilization time for 95% conversion [s]
    {'t_tkinf':12} {results['t_tkinf']:.2f} \t Time for particle center to reach T∞ [s]
    """
    print(textwrap.dedent(res_string))
