"""
Reactor model accounting for a distribution of particle sizes in one or more
CSTR reactors in series at steady-state conditions. Chemistry in each reactor
based on Liden 1988 kinetic scheme for biomass fast pyrolysis in a bubbling
fluidized bed reactor.

Test rxns- Based on Liden's (1988) kinetics
R1: W => t1*T (wood to tar), k1 = rate coeff. (1/s)
R2: T => g2*G (tar to gas), k2 = rate coeff. (1/s)
R3: W => c3*C + g3*G (wood to char + gas), k3 = rate coeff. (1/s)

Stagewise mass balances for each species:
dyW(i)/dt = -(k1+k3)*yW(i)+yW(i-1)/tau-yW(i)/tau => (Wood)
dyT(i)/dt = t1*k1*yW(i)-k2*yT(i)+yT(i-1)/tau-yT(i)/tau (Tar)
dyG(i)/dt = g2*k2*yT(i)+g3*k3*yW(i)+yG(i-1)/tau-yG(i)/tau (Gas)
dyC(i)/dt = c3*k3*yW(i)+yC(i-1)/tau-yC(i)/tau (Carbonized char)

Explicit s.s. solution to mass balances if done in proper sequence
General pattern yi = (i inflow + i gen rate*tau)/(1+i sink ks*tau)
yW = (1 + 0*tau)/(1+(k1+k3)*tau)
yT = (0 + t1*k1*yW*tau)/(1+k2*tau)
yG = (0 + g2*k2*yT+g3*k3*yW*tau)/(1+0)
yC = (0 + c3*k3*yW*tau)/(1+0)
"""

import numpy as np
import matplotlib.pyplot as py

# Parameters
# ------------------------------------------------------------------------------

T = 773             # reaction temperature, K
nstages = 10        # number of CSTR stages
taus = 4            # total solids residence time, s
taug = 0.5          # total gas residence time, s
yfw = 1             # normalized mass fraction of initial wood, (-)

# Particle Size Distribution Data
# ------------------------------------------------------------------------------

# load particle size distribution provided by Peter at NREL
file1 = 'sizeinfo.txt'
data = np.loadtxt(file1, skiprows=1, unpack=True)

data_vf2 = data[2]      # volume fractions for 2.0 mm sieve size, (-)
data_vf05 = data[3]     # volume fractions for 0.5 mm sieve size, (-)
data_v = data[4]        # volume of particles, m^3
data_sa = data[5]       # surface area of particles, m^2

# Functions
# ------------------------------------------------------------------------------


def cstr(T, nstages, taus, taug, tv, wood):
    tsn = taus / nstages    # solids residence time in each stage (s)
    tgn = taug / nstages    # gas residence time in each stage (s)
    Rgas = 8.314            # ideal gas constant (J/mole K)

    # kinetics parameters
    phi = 0.80      # Max tar yield fraction
    FC = 0.14       # Wt. fraction fixed C
    t1 = 1          # Tar mass formed/mass wood converted in rxn. 1
    g2 = 1          # Gas mass formed/mass tar converted in rxn. 2
    c3 = FC / (1 - phi)     # Char mass formed/mass wood converted in rxn. 3
    g3 = 1 - c3             # Gas mass formed/mass wood converted in rxn. 3
    k2 = 4.28e6 * np.exp(-107.5e3 / Rgas / T)    # Rxn. 2 rate coeff. (1/s)

    tvr = 0.54                                  # reference tau for Liden 1988
    k = 1e13 * np.exp(-183.3e3 / Rgas / T) * (tvr / tv)   # Sum of rxn. 1 & 3 rate coefficients (1/s)

    k1 = phi * k        # Rxn 1 rate constant (1/s)
    k3 = (1 - phi) * k  # Rxn. 3 rate constant (1/s)

    # Set up species solution vectors
    yW = yfw * np.ones(nstages)   # Unconverted wood (normalized to feed)
    yT = np.zeros(nstages)      # Tar (noramlized to feed)
    yG = np.zeros(nstages)      # Light gases (normalized to feed)
    yC = np.zeros(nstages)      # Char (normalized to feed)
    yCW = np.zeros(nstages)     # Char + wood (normalized to feed)

    # Mass balance for stage 1
    yW[1] = yfw / (1 + k * tsn)                         # Wood in exit
    yT[1] = t1 * k1 * yW[1] * tsn / (1 + k2 * tgn)      # Tar in exit
    yG[1] = g2 * k2 * yT[1] * tgn + g3 * k3 * yW[1] * tsn   # Gas in exit
    yC[1] = c3 * k3 * yW[1] * tsn                           # Carbonized char in exit
    yCW[1] = yW[1] + yC[1]          # Total carbonized char + uncoverted wood

    # Mass balances for remaining stages
    for i in range(2, nstages):
        yW[i] = yW[i - 1] / (1 + k * tsn)                                   # Wood in exit of stage i
        yT[i] = (yT[i - 1] + t1 * k1 * yW[i] * tsn) / (1 + k2 * tgn)        # Tar in exit of stage i
        yG[i] = yG[i - 1] + g2 * k2 * yT[i] * tgn + g3 * k3 * yW[i] * tsn   # Gas in exit
        yC[i] = yC[i - 1] + c3 * k3 * yW[i] * tsn                           # Carbonized char in exit
        yCW[i] = yC[i] + yW[i]                                              # Total wood + carbonized char

    return yW, yT, yG, yC


# Calculate Yields
# ------------------------------------------------------------------------------

# surface area, volume, and dsv for each particle size bin
ds = (data_sa / np.pi)**(1 / 2)     # surface area equivalent sphere diameter, m
dv = (6 / np.pi * data_v)**(1 / 3)  # volume equivalent sphere diameter, m
dsv = (dv**3) / (ds**2)             # surface area to volume sphere diameter, m

# devolatilization time for each bin
dsv = dsv * 1000  # convert m to mm
tv95 = 0.8 * np.exp(1525 / T) * (dsv * 1.2)


# yields from 0.5 mm sieve particle size distribution
wood05 = []
tar05 = []
gas05 = []
char05 = []

for tv in tv95:
    wood, tar, gas, char = cstr(T, nstages, taus, taug, tv, yfw)
    wood05.append(wood)
    tar05.append(tar)
    gas05.append(gas)
    char05.append(char)

wood05_wt = []
tar05_wt = []
gas05_wt = []
char05_wt = []

for (idx, vf) in enumerate(data_vf05):
    w = wood05[idx] * vf
    wood05_wt.append(w)
    t = tar05[idx] * vf
    tar05_wt.append(t)
    g = gas05[idx] * vf
    gas05_wt.append(g)
    c = char05[idx] * vf
    char05_wt.append(c)

wood05_sum = sum(wood05_wt)
tar05_sum = sum(tar05_wt)
gas05_sum = sum(gas05_wt)
char05_sum = sum(char05_wt)

# yields from 2.0 mm sieve particle size distribution
wood20 = []
tar20 = []
gas20 = []
char20 = []

for tv in tv95:
    wood, tar, gas, char = cstr(T, nstages, taus, taug, tv, yfw)
    wood20.append(wood)
    tar20.append(tar)
    gas20.append(gas)
    char20.append(char)

wood20_wt = []
tar20_wt = []
gas20_wt = []
char20_wt = []

for (idx, vf) in enumerate(data_vf2):
    w = wood20[idx] * vf
    wood20_wt.append(w)
    t = tar20[idx] * vf
    tar20_wt.append(t)
    g = gas20[idx] * vf
    gas20_wt.append(g)
    c = char20[idx] * vf
    char20_wt.append(c)

wood20_sum = sum(wood20_wt)
tar20_sum = sum(tar20_wt)
gas20_sum = sum(gas20_wt)
char20_sum = sum(char20_wt)

# don't forget to check mass balances

# Print Product Yields
# ------------------------------------------------------------------------------

print('- 0.5 mm sieve yields (top of reactor) -')
print('wood = ', wood05_sum[-1] * 100)
print('tar = ', tar05_sum[-1] * 100)
print('gas = ', gas05_sum[-1] * 100)
print('char = ', char05_sum[-1] * 100)
print('mass balance = ', wood05_sum + tar05_sum + gas05_sum + char05_sum)

print('- 2.0 mm sieve yields (top of reactor) -')
print('wood = ', wood20_sum[-1] * 100)
print('tar = ', tar20_sum[-1] * 100)
print('gas = ', gas20_sum[-1] * 100)
print('char = ', char20_sum[-1] * 100)
print('mass balance = ', wood20_sum + tar20_sum + gas20_sum + char20_sum)

# Plot Results
# ------------------------------------------------------------------------------

ns = range(nstages)     # list for numbers of stages


def despine():
    ax = py.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    py.tick_params(bottom=False, top=False, left=False, right=False)
    py.grid()


py.figure(figsize=(5, 8))
py.plot(tar05_sum, ns, lw=2, label='0.5 mm model')
py.plot(tar20_sum, ns, lw=2, label='2.0 mm model')
py.axvline(0.71, c='b', ls='--', lw=2, label='0.5 mm sieve')
py.axvline(0.64, c='g', ls='--', lw=2, label='2.0 mm sieve')
py.xlim([0, 0.80])
py.xlabel('Tar Yield (wt. fraction)')
py.ylabel('Reactor Height (stage number)')
py.title('Distribution of Particle Sizes')
py.legend(loc='best', numpoints=1, fontsize='medium', frameon=False)
despine()

py.show()
