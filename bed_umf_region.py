"""
here
"""

import chemics as cm
import matplotlib.pyplot as plt
import numpy as np

p_gas = 101_325
tk_gas = 773.15

dp = np.arange(300, 600 + 20, 20)
temp = np.arange(723, 823 + 10, 10)

mw_n2 = cm.molecular_weight('N2')


def umf(d, t):
    mu_n2 = cm.mu_gas('N2', t) * 1e-7
    rho_n2 = cm.rhog(mw_n2, p_gas, t)
    u = cm.umf_ergun(d * 1e-6, 0.46, mu_n2, 0.8, rho_n2, 2500)
    return u


v_umf = np.vectorize(umf)

x, y = np.meshgrid(dp, temp)
z = v_umf(x, y)

fig, ax = plt.subplots()
cs = ax.contourf(x, y, z)
ax.set_frame_on(False)
ax.set_title('Nitrogen Gas')
ax.set_xlabel('Diameter [um]')
ax.set_ylabel('Temperature [K]')
cbar = fig.colorbar(cs)
cbar.ax.set_ylabel('Umf [m/s]')

plt.show()
