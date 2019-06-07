"""
Parameters for modeling the BFB pyrolysis reactor in the NREL 2FBR system.
"""

# Simulation
# ----------------------------------------------------------------------------

sim = {
    'b': 2,         # Shape factor for particle transient heat conduction [-]
    'm': 1000,      # Number of nodes from particle center (m=0) to surface (m)
    'nt': 1000,     # Number of time steps for particle temperature profile
    'tmax': 6.0,    # Time duration to calculate particle temperature profile [s]
}

# Bed Conditions
# ----------------------------------------------------------------------------

bed = {
    'dps': (0.0003, 0.0002, 0.0005),    # Mean, min, max particle diameter [m]
    'ep': 0.45,                         # Void fraction of bed [-]
    'phi': 0.86,                        # Sphericity of a bed particle [-]
    'rhos': 2500,                       # Density of a bed particle [kg/m³]
    'zmf': 0.1016                       # Bed height at minimum fluidization [m]
}

# Feedstock Conditions
# ----------------------------------------------------------------------------

# sg from Wood Handbook Table 4-7

feed = {
    'dp_mean': 0.0005,  # Mean particle diameter [m]
    'h': 350,           # Heat transfer coefficient to feedstock in bed [W/m²K]
    'k': 0.11,          # Thermal conductivity [W/mK]
    'mc': 0,            # Moisture content [%]
    'sg': 0.54,         # Specific gravity of loblolly pine [-]
    'ti': 293.15        # Initial particle temperature [K]
}

# Gas Conditions
# ----------------------------------------------------------------------------

gas = {
    'p': 101_325,           # Gas pressure in reactor [Pa]
    'q': 14,                # Volumetric flowrate of gas into reactor [SLM]
    'tk': 773.15,           # Gas temperature in reactor [K]
    'sp': ['H2', 'N2'],     # Gas species of each component in gas mixture [-]
    'x': [0.85, 0.15],      # Mole fraction of each component in gas mixture [-]
}

# Reactor Geometry
# ----------------------------------------------------------------------------

reactor = {
    'di': 0.05232,          # Inner diameter of reactor [m]
}
