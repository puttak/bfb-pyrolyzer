"""
Parameters for modeling the BFB biomass pyrolysis reactor in the NREL 2FBR
system.
"""

# Simulation
# ----------------------------------------------------------------------------

sim = {
    'b': 2,                     # Shape factor for particle transient heat conduction [-]
    'm': 1000,                  # Number of nodes from particle center (m=0) to surface (m)
    'nt': 1000,                 # Number of time steps for particle temperature profile
    'tmax': 6.0,                # Time duration to calculate particle temperature profile [s]
    'tks': (723.15, 823.15),    # Temperature range [K]
    'ps': (101_325, 150_000),   # Pressure range [Pa]
    'qs': (14, 24),             # Volumetric flow range [SLM]
}

# Bed Conditions and Properties
# ----------------------------------------------------------------------------

bed = {
    'dps': (0.0003, 0.0002, 0.0005),    # Mean, min, max particle diameter [m]
    'ep': 0.45,                         # Void fraction of bed [-]
    'phi': 0.86,                        # Sphericity of a bed particle [-]
    'rhos': 2500,                       # Density of a bed particle [kg/m³]
    'zmf': 0.1016                       # Bed height at minimum fluidization [m]
}

# Biomass Conditions and Properties
# ----------------------------------------------------------------------------

# Specific gravity and thermal conductivity from Wood Handbook Table 4-7

biomass = {
    'dp_mean': 0.0005,  # Mean particle diameter [m]
    'h': 350,           # Heat transfer coefficient for convection [W/m²K]
    'k': 0.12,          # Thermal conductivity of loblolly pine [W/mK]
    'mc': 0.0,          # Moisture content [%]
    'sg': 0.54,         # Specific gravity of loblolly pine [-]
    'ti': 293.15        # Initial particle temperature [K]
}

# Gas Conditions
# ----------------------------------------------------------------------------

gas = {
    'p': 101_325,           # Gas pressure in reactor [Pa]
    # 'q': 14,                # Volumetric flowrate of gas into reactor [SLM]
    'q': 20,                # Volumetric flowrate of gas into reactor [SLM]
    'tk': 773.15,           # Gas temperature in reactor [K]
    'sp': ['H2', 'N2'],     # Gas species of each component in gas mixture [-]
    'x': [0.85, 0.15],      # Mole fraction of each component in gas mixture [-]
    # 'sp': 'N2',             # Gas species of each component in gas mixture [-]
    # 'x': 1.0,               # Mole fraction of each component in gas mixture [-]
}

# Reactor Geometry
# ----------------------------------------------------------------------------

reactor = {
    'di': 0.05232,          # Inner diameter of reactor [m]
}
