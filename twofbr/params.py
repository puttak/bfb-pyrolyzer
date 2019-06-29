"""
Parameters for modeling the BFB biomass pyrolysis reactor in the NREL 2FBR
system.
"""

# Cases to Simulate
# ----------------------------------------------------------------------------

case = {
    'p': (101_325, 150_000),            # Pressure range [Pa]
    'q': (14, 24),                      # Volumetric flow range [SLM]
    'tk': (723.15, 823.15)              # Temperature range [K]
}

# Bed Conditions and Properties
# ----------------------------------------------------------------------------

bed = {
    'dp': 0.0003,           # Mean particle diameter [m]
    'dp_min': 0.0002,       # Minimum particle diameter [m]
    'dp_max': 0.0005,       # Maximum particle diameter [m]
    'phi': 0.86,            # Sphericity [-]
    'rho': 2500             # Density [kg/m³]
}

# Biomass Conditions and Properties
# ----------------------------------------------------------------------------

# Specific gravity and thermal conductivity from Wood Handbook Table 4-7

biomass = {
    'dp': 0.0005,           # Mean particle diameter [m]
    'phi': 0.6,             # Sphericity of biomass particle [-]
    'sg': 0.54,             # Specific gravity of loblolly pine [-]
    'b': 2,                 # Shape factor for particle transient heat conduction [-]
    'h': 350,               # Heat transfer coefficient for convection [W/m²K]
    'k': 0.12,              # Thermal conductivity of loblolly pine [W/mK]
    'm': 1000,              # Number of nodes from particle center (m=0) to surface (m)
    'mc': 0.0,              # Moisture content [%]
    'nt': 1000,             # Number of time steps for particle temperature profile [-]
    'tki': 293.15,          # Initial particle temperature [K]
    't_max': 6              # Time duration to calculate particle temperature profile [s]
}

# Char particle
# ----------------------------------------------------------------------------

char = {
    'dp': 0.0005,       # Mean particle diameter [m]
    'phi': 0.6,         # Sphericity [-]
    'rho': 120          # Density [kg/m³]
}

# Gas Conditions
# ----------------------------------------------------------------------------

gas = {
    'sp': ['H2', 'N2'],     # Gas species of each component in gas mixture [-]
    'x': [0.85, 0.15],      # Mole fraction of each component in gas mixture [-]
    'p': 101_325,           # Gas pressure in reactor [Pa]
    'tk': 773.15            # Gas temperature in reactor [K]
}

# Reactor Geometry and Conditions
# ----------------------------------------------------------------------------

reactor = {
    'di': 0.05232,      # Inner diameter of reactor [m]
    'ep': 0.45,         # Void fraction of bed material [-]
    'ht': 0.4318,       # Total height of reactor [m]
    'q': 14,            # Volumetric flowrate of gas into reactor [SLM]
    'zmf': 0.1016       # Bed height at minimum fluidization [m]
}
