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

# Gas mixture properties
# ----------------------------------------------------------------------------


def mix_props(params):

    mix_formulas = params.mix_formulas
    wts = params.mix_wts
    p = params.p_gas
    tk = params.tk_gas

    gas_mixtures = []

    for idx, mix in enumerate(mix_formulas):
        gas_mix = rct.GasMixture(mix, p, tk, wts[idx])
        gas_mixtures.append(gas_mix)

    return gas_mixtures


mixtures = mix_props(params)

# Print and plot results
# ----------------------------------------------------------------------------

rct.print_params('Pyrolyzer Parameters', params)

rct.plot_mixture_properties(mixtures, params.mix_wts)
rct.show_plots()
