"""
BFB pyrolysis reactor in the NREL 2FBR system.
"""

import numpy as np
import bfbreactor as rct

# Parameters
# ----------------------------------------------------------------------------

params = rct.params

# temperature range for calculations [°C]
tc = np.arange(440, 570, 10)

# Bed properties such as umf and bed expansion
# ----------------------------------------------------------------------------


def calc_umf_zexp(params, tc):

    bfb = rct.Bfb(params)
    gas_formulas = params.gas_formulas
    p = params.p_gas
    xumf = params.xumf

    umf_array = np.zeros([len(gas_formulas), len(tc)])
    zexp_array = np.zeros([len(gas_formulas), len(tc)])

    for i, formula in enumerate(gas_formulas):
        for j, t in enumerate(tc):
            tk = t + 273.15
            gas = rct.Gas(formula, p, tk)
            umf = bfb.calc_umf(gas)
            us = bfb.calc_us(umf, xumf)
            umf_array[i, j] = umf
            zexp_array[i, j] = bfb.calc_zexp(gas, umf, us)

    return umf_array, zexp_array


def calc_umf_zexp_mix(params, tc):

    bfb = rct.Bfb(params)
    mix_formulas = params.mix_formulas
    mix_wts = params.mix_wts
    p = params.p_gas
    xumf = params.xumf

    umf_array = np.zeros([len(mix_formulas), len(tc)])
    zexp_array = np.zeros([len(mix_formulas), len(tc)])

    for i, mix_formula in enumerate(mix_formulas):
        for j, t in enumerate(tc):
            tk = t + 273.15
            gas_mix = rct.GasMixture(mix_formula, p, tk, mix_wts[i])
            umf = bfb.calc_umf(gas_mix)
            us = bfb.calc_us(umf, xumf)
            umf_array[i, j] = umf
            zexp_array[i, j] = bfb.calc_zexp(gas_mix, umf, us)

    return umf_array, zexp_array


umf_gases, zexp_gases = calc_umf_zexp(params, tc)
umf_mixtures, zexp_mixtures = calc_umf_zexp_mix(params, tc)

# Print and plot results
# ----------------------------------------------------------------------------

rct.print_params('Pyrolyzer Parameters', params)

rct.plot_umf_zexp(params.gas_formulas, tc, umf_gases, zexp_gases)
rct.plot_umf_zexp(params.mix_formulas, tc, umf_mixtures, zexp_mixtures)
rct.show_plots()
