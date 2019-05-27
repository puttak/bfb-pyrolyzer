"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

# Gas
# ----------------------------------------------------------------------------

# Gas species
gas = ['H2', 'N2']

# Mole fractions of gas mixture [-]
xgas = [0.85, 0.15]

# Gas pressure in reactor [Pa]
pgas = 101_325

# Gas temperature in reactor [K]
tgas = 773.15

# Feedstock
# ----------------------------------------------------------------------------


# Bed
# ----------------------------------------------------------------------------

# Mean particle diameter [m], min and max particle diameter [m]
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
