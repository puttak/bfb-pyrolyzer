"""
Calculate gas properties of individual gases and gas mixtures. Selected gases
are based on the ones presented in the Mullen 2013 paper.

References
----------
Charles A. Mullen, Akwasi A. Boateng, and Neil M. Goldberg. Production of
Deoxygenated Biomass Fast Pyrolysis Oils via Product Gas Recycling. Energy and
Fuels, 2013.
"""

import bfbreactor as rct

# Parameters
# ----------------------------------------------------------------------------

params = rct.params

# Gas properties
# ----------------------------------------------------------------------------


def gas_props(params):

    gas_formulas = params.gas_formulas
    p = params.p_gas
    tk = params.tk_gas

    gases = []

    for formula in gas_formulas:
        gas = rct.Gas(formula, p, tk)
        gases.append(gas)

    return gases


gases = gas_props(params)

# Print and plot results
# ----------------------------------------------------------------------------

rct.print_params('Pyrolyzer Parameters', params)

rct.plot_gas_properties(gases)
rct.show_plots()
