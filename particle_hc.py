"""
Intraparticle heat conduction within woody biomass particle at fast pyrolysis
conditions.
"""

import numpy as np
import matplotlib.pyplot as plt
import bfbreactor as rct


# Parameters
# ------------------------------------------------------------------------------

Gb = 0.46       # basic specific gravity, Wood Handbook Table 4-7, (-)
k = 0.11        # thermal conductivity, W/mK
x = 0           # moisture content, %
h = 350         # heat transfer coefficient, W/m^2*K
Ti = 293        # initial particle temp, K
Tinf = 773      # ambient temp, K

# number of nodes from center of particle (m=0) to surface (m)
m = 1000

# time vector from 0 to max time
tmax = 6.0                          # max time, s
nt = 1000                           # number of time steps
dt = tmax / nt                      # time step, s
t = np.arange(0, tmax + dt, dt)     # time vector, s

# 1D Transient Heat Conduction
# ------------------------------------------------------------------------------

# Calculate temperature profiles within particle.
# rows = time step, columns = center to surface temperature
T = rct.hc2(0.0005, x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K

# Determine time when particle has reached near reactor temperature. Assume
# this time is when particle has converted from wood to char thus fully
# devolatilized.
idx770 = np.where(T[:, 0] > 770)[0][0]  # index where T > 770 K
t770 = t[idx770]                        # time where T > 770 K
print('t at T > 770 K is {} s'.format(t770))

# Plot Results
# ------------------------------------------------------------------------------

plt.figure()
plt.plot(t, T[:, 0], lw=2, label='center')
plt.plot(t, T[:, -1], lw=2, label='surface')
plt.axvline(t770, c='r', label='T > 770 K')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend(loc='lower right', numpoints=1)
plt.grid()

plt.show()
