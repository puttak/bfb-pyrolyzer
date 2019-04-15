"""
Plot center and surface temperatue profiles for a distribution of particle
sizes where the particle size distribution (PSD) is divided into nine bins.
Estimate conversion time of each bin based on time for center temperature to
reach 770 K. Wood properties based on loblolly pine data from Wood Handbook.

Reference:
Wood Handbook, 2010, Table 4-7.
"""

import numpy as np
import matplotlib.pyplot as plt
import bfbreactor as rct

# Parameters
# ------------------------------------------------------------------------------

Gb = 0.54       # basic specific gravity loblolly pine, Wood Handbook Table 4-7
k = 0.12        # thermal conductivity, W/mK, Wood Handbook Table 4-7
x = 0           # moisture content, %
h = 350         # heat transfer coefficient, W/m^2*K
Ti = 293        # initial particle temp, K
Tinf = 773      # ambient temp, K

# number of nodes from center of particle (m=0) to surface (m)
m = 1000

# time vector from 0 to max time
tmax = 2.0                      # max time, s
nt = 1000                       # number of time steps
dt = tmax / nt                    # time step, s
t = np.arange(0, tmax + dt, dt)   # time vector, s

# Particle Size Distribution Data
# ------------------------------------------------------------------------------

# load particle size distribution provided by Peter at NREL
file1 = 'sizeinfo.txt'
data = np.loadtxt(file1, skiprows=1, unpack=True)

# data_vf2 = data[2]      # volume fractions for 2.0 mm sieve size, (-)
# data_vf05 = data[3]     # volume fractions for 0.5 mm sieve size, (-)
data_v = data[4]        # volume of particles for each bin, m^3 [vector]
data_sa = data[5]       # surface area of particles for each bin, m^2 [vector]

# 1D Transient Heat Conduction
# ------------------------------------------------------------------------------

# surface area, volume, and dsv for each particle size bin
ds = (data_sa / np.pi)**(1 / 2)     # surface area equivalent sphere diameter, m
dv = (6 / np.pi * data_v)**(1 / 3)  # volume equivalent sphere diameter, m
dsv = (dv**3) / (ds**2)             # surface area to volume sphere diameter, m

# Calculate temperature profiles in particle with diameter of Dsv for each bin.
# rows = time step, columns = center to surface temperature
T0 = rct.hc2(dsv[0], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T1 = rct.hc2(dsv[1], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T2 = rct.hc2(dsv[2], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T3 = rct.hc2(dsv[3], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T4 = rct.hc2(dsv[4], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T5 = rct.hc2(dsv[5], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T6 = rct.hc2(dsv[6], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T7 = rct.hc2(dsv[7], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K
T8 = rct.hc2(dsv[8], x, k, Gb, h, Ti, Tinf, 2, m, t)    # temperature array, K

# Determine time when particle has reached near reactor temperature. Assume
# this time is when particle has converted from wood to char thus fully
# devolatilized.
idx0 = np.where(T0[:, 0] > 770)[0][0]   # index where T > 770 K
t0 = t[idx0]                            # time where T > 770 K

idx1 = np.where(T1[:, 0] > 770)[0][0]   # index where T > 770 K
t1 = t[idx1]                            # time where T > 770 K

idx2 = np.where(T2[:, 0] > 770)[0][0]   # index where T > 770 K
t2 = t[idx2]                            # time where T > 770 K

idx3 = np.where(T3[:, 0] > 770)[0][0]   # index where T > 770 K
t3 = t[idx3]                            # time where T > 770 K

idx4 = np.where(T4[:, 0] > 770)[0][0]   # index where T > 770 K
t4 = t[idx4]                            # time where T > 770 K

idx5 = np.where(T5[:, 0] > 770)[0][0]   # index where T > 770 K
t5 = t[idx5]                            # time where T > 770 K

idx6 = np.where(T6[:, 0] > 770)[0][0]   # index where T > 770 K
t6 = t[idx6]                            # time where T > 770 K

idx7 = np.where(T7[:, 0] > 770)[0][0]   # index where T > 770 K
t7 = t[idx7]                            # time where T > 770 K

idx8 = np.where(T8[:, 0] > 770)[0][0]   # index where T > 770 K
t8 = t[idx8]                            # time where T > 770 K

print('t0 at T > 770 K is {:g} s'.format(t0))
print('t1 at T > 770 K is {:g} s'.format(t1))
print('t2 at T > 770 K is {:g} s'.format(t2))
print('t3 at T > 770 K is {:g} s'.format(t3))
print('t4 at T > 770 K is {:g} s'.format(t4))
print('t5 at T > 770 K is {:g} s'.format(t5))
print('t6 at T > 770 K is {:g} s'.format(t6))
print('t7 at T > 770 K is {:g} s'.format(t7))
print('t8 at T > 770 K is {:g} s'.format(t8))

# Plot Results
# ------------------------------------------------------------------------------

plt.figure()
plt.plot(t, T0[:, 0], lw=2, label='center')
plt.plot(t, T0[:, -1], lw=2, label='surface')
plt.axvline(t0, c='r', label='T > 770 K')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend(loc='lower right', numpoints=1)
plt.grid()

plt.figure()
plt.plot(t, T8[:, 0], lw=2, label='center')
plt.plot(t, T8[:, -1], lw=2, label='surface')
plt.axvline(t8, c='r', label='T > 770 K')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.legend(loc='lower right', numpoints=1)
plt.grid()

plt.show()
