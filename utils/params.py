"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

# Gas
# ----------------------------------------------------------------------------

# Gas species where CH4 is methane, C2H6 is ethane, and C3H8 is propane
gas = ['CH4', 'CO', 'CO2', 'C2H6', 'C3H8', 'H2', 'N2']

# Gas mixtures where each item is a mixture of two gases
mix = [('H2', 'N2'), ('CO', 'N2'), ('CO', 'N2'), ('C2H6', 'N2')]

# Weights for gas mixture where each item is fraction of the two gases [-]
wts = [(0.8, 0.2), (0.7, 0.3), (0.3, 0.7), (0.8, 0.2)]

# Gas pressure in reactor [Pa]
pgas = 101_325

# Gas temperature in reactor [K]
tgas = 773.15

# Feedstock
# ----------------------------------------------------------------------------


# Bed
# ----------------------------------------------------------------------------

# Mean particle diameter [m]
dp = 0.0003

# Void fraction of bed [-]
ep = 0.45

# Particle sphericity [-]
phi = 0.86

# Density of a bed particle [kg/m^3]
rhos = 2500

# Bed height at minimum fluidization [m]
zmf = 0.1016

# Reactor
# ----------------------------------------------------------------------------

# Inner diameter of reactor [m]
di = 0.05232

# Diameter of orifice in distributor plate [m]
dorif = 0.0008
