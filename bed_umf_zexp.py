"""
Minimum fluidization velocity for individual gases and gas mixtures.
Calculations are for a range of temperatures.
"""

import matplotlib.pyplot as plt
import numpy as np
import chemics as cm
import utils

# Parameters
# ----------------------------------------------------------------------------

di = utils.params.di
dp = utils.params.dp
ep = utils.params.ep
gas = utils.params.gas
mix = utils.params.mix
pgas = utils.params.pgas
phi = utils.params.phi
rhos = utils.params.rhos
wts = utils.params.wts
zmf = utils.params.zmf

# Minimum fluidization velocity and bed expansion
# ----------------------------------------------------------------------------

# temperature range for calculations [°C]
tc = np.arange(450, 560, 10)

ngas = len(gas)
nmix = len(mix)
ntc = len(tc)

umf_gases = np.zeros([ngas, ntc])
zexp_gases = np.zeros([ngas, ntc])

umf_mixes = np.zeros([nmix, ntc])
zexp_mixes = np.zeros([nmix, ntc])

# calculations for a single gas
for i in range(ngas):
    mw = cm.molecular_weight(gas[i])

    for j in range(ntc):
        tk = tc[j] + 273.15

        mu = cm.mu_gas(gas[i], tk) * 1e-7
        rhog = cm.rhog(mw, pgas, tk)
        umf = cm.umf_ergun(dp, ep, mu, phi, rhog, rhos)
        umf_gases[i, j] = umf

        us = 3 * umf
        fbexp = cm.fbexp(di, dp, rhog, rhos, umf, us)
        zexp_gases[i, j] = zmf * fbexp

# calculations for a gas mixture
for i in range(nmix):
    mw_mix = cm.mw_mix(mix[i], wts[i])

    for j in range(ntc):
        tk = tc[j] + 273.15

        mu = cm.mu_gas_mix(mix[i], tk, wts[i]) * 1e-7
        rhog = cm.rhog(mw_mix, pgas, tk)
        umf = cm.umf_ergun(dp, ep, mu, phi, rhog, rhos)
        umf_mixes[i, j] = umf

        us = 3 * umf
        fbexp = cm.fbexp(di, dp, rhog, rhos, umf, us)
        zexp_mixes[i, j] = zmf * fbexp

# Plot
# ----------------------------------------------------------------------------

sub = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')

fig, ax = plt.subplots(tight_layout=True)
for i in range(ngas):
    ax.plot(tc, umf_gases[i], marker='.', label=gas[i].translate(sub))
ax.grid(True, color='0.9')
ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, frameon=False)
ax.set_frame_on(False)
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Minimum fluidization velocity [m/s]')
ax.tick_params(color='0.9')

fig, ax = plt.subplots(tight_layout=True)
for i in range(ngas):
    ax.plot(umf_gases[i], zexp_gases[i], marker='.', label=gas[i].translate(sub))
ax.grid(True, color='0.9')
ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, frameon=False)
ax.set_frame_on(False)
ax.set_xlabel('Minimum fluidization velocity [m/s]')
ax.set_ylabel('Bed expansion [m]')
ax.tick_params(color='0.9')

mixtures = ['+'.join(m) for m in mix]

fig, ax = plt.subplots(tight_layout=True)
for i in range(nmix):
    ax.plot(tc, umf_mixes[i], marker='.', label=mixtures[i].translate(sub))
ax.grid(True, color='0.9')
ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, frameon=False)
ax.set_frame_on(False)
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Minimum fluidization velocity [m/s]')
ax.tick_params(color='0.9')

fig, ax = plt.subplots(tight_layout=True)
for i in range(nmix):
    ax.plot(umf_mixes[i], zexp_mixes[i], marker='.', label=mixtures[i].translate(sub))
ax.grid(True, color='0.9')
ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, frameon=False)
ax.set_frame_on(False)
ax.set_xlabel('Minimum fluidization velocity [m/s]')
ax.set_ylabel('Bed expansion [m]')
ax.tick_params(color='0.9')

# plt.subplots_adjust(right=0.8)
plt.show()
