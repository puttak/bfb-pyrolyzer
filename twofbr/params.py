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
    'dp': (0.0003, 0.0002, 0.0005),     # Mean, min, max particle diameter [m]
    'ep': 0.45,                         # Void fraction of bed [-]
    'phi': 0.86,                        # Sphericity of a bed particle [-]
    'rhos': 2500,                       # Density of a bed particle [kg/m³]
    'rhos_char': 120,                   # Density of a char particle [kg/m³]
    'zmf': 0.1016                       # Bed height at minimum fluidization [m]
}

# Biomass Conditions and Properties
# ----------------------------------------------------------------------------

# Specific gravity and thermal conductivity from Wood Handbook Table 4-7

biomass = {
    'dp_mean': 0.0005,         # Mean particle diameter [m]
    'h': 350,                  # Heat transfer coefficient for convection [W/m²K]
    'k': 0.12,                 # Thermal conductivity of loblolly pine [W/mK]
    'mc': 0.0,                 # Moisture content [%]
    'phi': 0.6,                # Sphericity of biomass particle [-]
    'sg': 0.54,                # Specific gravity of loblolly pine [-]
    'tk_i': 293.15,            # Initial particle temperature [K]
    'b': 2,                    # Shape factor for particle transient heat conduction [-]
    'm': 1000,                 # Number of nodes from particle center (m=0) to surface (m)
    'nt': 1000,                # Number of time steps for particle temperature profile
    't_max': 6                 # Time duration to calculate particle temperature profile [s]
}

# Gas Conditions
# ----------------------------------------------------------------------------

gas = {
    'p': 101_325,           # Gas pressure in reactor [Pa]
    'q': 14,                # Volumetric flowrate of gas into reactor [SLM]
    'sp': ['H2', 'N2'],     # Gas species of each component in gas mixture [-]
    'tk': 773.15,           # Gas temperature in reactor [K]
    'x': [0.85, 0.15]       # Mole fraction of each component in gas mixture [-]
}

# Reactor Geometry
# ----------------------------------------------------------------------------

reactor = {
    'di': 0.05232,      # Inner diameter of reactor [m]
    'ht': 0.4318        # Total height of reactor [m]
}
