"""
here
"""

import chemics as cm
import matplotlib.pyplot as plt
import numpy as np
import utils


def mu_herning(mu, mw, x):
    mu = np.sum(mu * x * np.sqrt(mw)) / np.sum(x * np.sqrt(mw))
    return mu


# parameters
dp = utils.params.dp
ep = utils.params.ep
pgas = utils.params.pgas
phi = utils.params.phi
rhos = utils.params.rhos

# temperature range for calculations [°C]
tc = np.arange(450, 560, 10)

# mole fractions
x_mix = np.array([0.85, 0.15])

# molecular weight
mw_h2 = cm.molecular_weight('H2')
mw_n2 = cm.molecular_weight('N2')
mw_mix = cm.mw_mix(('H2', 'N2'), x_mix)

# minimum fluidization velocity [m/s]
umf_h2 = []
umf_n2 = []
umf_mix = []

for t in tc:
    tk = t + 273.15

    mu_h2 = cm.mu_gas('H2', tk) * 1e-7
    mu_n2 = cm.mu_gas('N2', tk) * 1e-7
    mu_h2_n2 = np.array([mu_h2, mu_n2])
    mu_mix = mu_herning(mu_h2_n2, mw_mix, x_mix)

    rhog_h2 = cm.rhog(mw_h2, pgas, tk)
    rhog_n2 = cm.rhog(mw_n2, pgas, tk)
    rhog_mix = cm.rhog(mw_mix, pgas, tk)

    umf_h2.append(cm.umf_ergun(dp, ep, mu_h2, phi, rhog_h2, rhos))
    umf_n2.append(cm.umf_ergun(dp, ep, mu_n2, phi, rhog_n2, rhos))
    umf_mix.append(cm.umf_ergun(dp, ep, mu_mix, phi, rhog_mix, rhos))

# plot
fig, ax = plt.subplots(tight_layout=True)
ax.plot(tc, umf_h2, marker='.', label='H₂')
ax.plot(tc, umf_n2, marker='.', label='N₂')
ax.plot(tc, umf_mix, marker='.', label='0.85H₂, 0.15N₂')
ax.grid(color='0.9')
ax.legend(frameon=False, loc='best')
ax.set_frame_on(False)
ax.set_xlabel('Temperature [°C]')
ax.set_ylabel('Minimum fluidization velocity [m/s]')
ax.tick_params(color='0.9')

plt.show()
