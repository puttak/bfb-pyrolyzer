"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

# Bed
# ----------------------------------------------------------------------------

bed = {
    'dp_mean': 0.0003,  # Mean particle diameter [m]
    'dp_min': 0.0002,   # Min particle diameter [m]
    'dp_max': 0.0005,   # Max particle diameter [m]
    'ep': 0.45,         # Void fraction of bed [-]
    'phi': 0.86,        # Particle sphericity [-]
    'rho': 2500,        # Density of a bed particle [kg/m³]
    'zmf': 0.1016       # Bed height at minimum fluidization [m]
}

# Feedstock
# ----------------------------------------------------------------------------

feedstock = {
    'dp': 0.0005    # Mean particle diameter of biomass feedstock [m]
}

# Gas
# ----------------------------------------------------------------------------

gas = {
    'species': ['H2', 'N2'],    # Gas species of each component in gas mixture [-]
    'x': [0.85, 0.15],          # Mole fraction of each component in gas mixture [-]
    'p': 101_325,               # Gas pressure in reactor [Pa]
    'q': 14,                    # Volumetric flowrate of gas into reactor [SLM]
    't': 773.15                 # Gas temperature in reactor [K]
}

# Reactor
# ----------------------------------------------------------------------------

reactor = {
    'di': 0.05232   # Inner diameter of reactor [m]
}
