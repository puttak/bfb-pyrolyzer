"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

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

# Gas
# ----------------------------------------------------------------------------

# Gas species
gas = ['H2', 'N2']

# Gas pressure in reactor [Pa]
p_gas = 101_325

# Volumetric flowrate of gas into reactor [SLM]
q_gas = 14

# Gas temperature in reactor [K]
t_gas = 773.15

# Mole fractions of gas mixture [-]
x_gas = [0.85, 0.15]
# x_gas = [0.0, 1.0]

# Reactor
# ----------------------------------------------------------------------------

# Inner diameter of reactor [m]
di = 0.05232
