"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

# Gas phase
# ----------------------------------------------------------------------------

# Gas formulas where each item is a single gas.
# CH4 is methane, C2H6 is ethane, and C3H8 is propane.
gas_formulas = ['CH4', 'CO', 'CO2', 'H2', 'N2', 'C2H6', 'C3H8']

# Gas mixtures where each item is a mixture of two gases.
mix_formulas = [('H2', 'N2'), ('CO', 'N2'), ('CO', 'N2'), ('C2H6', 'N2')]

# Weights for gas mixture where each item is fraction of the two gases [-]
mix_wts = [(0.8, 0.2), (0.7, 0.3), (0.3, 0.7), (0.8, 0.2)]

# Pressure of gas in the reactor [Pa]
p_gas = 115000

# Temperature of gas in the reactor [K]
tk_gas = 773.15

# Solid phase
# ----------------------------------------------------------------------------

# Diameter of bed particles [m]
dp = 0.000300

# Void fraction of the bed [-]
ep = 0.45

# Sphericity of bed particles [-]
phi = 0.86

# Density of the bed particles [kg/m^3]
rhos = 2500

# Reactor geometry and conditions
# ----------------------------------------------------------------------------

# Inner reactor diameter [m]
d_inner = 0.05232

# Factor to determine superficial gas velocity where Us = xumf * Umf [-]
xumf = 3

# Bed height at minimum fluidization [m]
zmf = 0.1016
