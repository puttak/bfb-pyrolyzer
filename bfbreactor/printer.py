import textwrap


def print_params(name, pm):
    """
    Print parameters.
    """

    pm_string = f"""
    === {name} ===

    --- Gas Phase ---
    {'gas formulas':15} {pm.gas_formulas}
    {'mix formulas':15} {pm.mix_formulas}
    {'mix weights':15} {pm.mix_wts}
    {'p_gas':10} {pm.p_gas:>12} \t pressure of gas in reactor [Pa]
    {'tk_gas':10} {pm.tk_gas:>12} \t temperature gas in reactor [K]

    --- Solid Phase ---
    {'dp':10} {pm.dp:>12} \t diameter of bed particles [m]
    {'ep':10} {pm.ep:>12} \t void fraction of the bed [-]
    {'phi':10} {pm.phi:>12} \t sphericity of bed particles [-]
    {'rhos':10} {pm.rhos:>12} \t density of bed particles [kg/m³]

    --- BFB Reactor ---
    {'d_inner':10} {pm.d_inner:>12} \t inner reactor diameter [m]
    {'xumf':10} {pm.xumf:>12} \t factor for Us where Us = xumf * Umf [-]
    {'zmf':10} {pm.zmf:>12} \t bed height at minimum fluidization [m]
    """

    params_dedent = textwrap.dedent(pm_string)
    print(params_dedent)
