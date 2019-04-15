"""
Devolatlization time for BFB pyrolysis reactor in the NREL 2FBR system.
"""

import chemics as cm
import numpy as np
import bfbreactor as rct

# Parameters
# ----------------------------------------------------------------------------

params = rct.params

# Devolatilization times at different bed temperatures
# ----------------------------------------------------------------------------

dp = np.linspace(0.1, 5)  # particle diameters, mm [vector]

# devolatilization times for 95% conversion
dv1 = cm.devol_time(dp, 723.15)     # 723.15 K (450°C) bed temperature
dv2 = cm.devol_time(dp, 773.15)     # 773.15 K (500°C) bed temperature
dv3 = cm.devol_time(dp, 823.15)     # 823.15 K (550°C) bed temperature
dv4 = cm.devol_time(dp, 873.15)     # 873.15 K (600°C) bed temperature
dv_tbed = dv1, dv2, dv3, dv4

# Devolatilization times for different diameters
# -----------------------------------------------------------------------------

tbed = np.linspace(723.15, 923.15)  # bed temperatures, K [vector]

# devolatilization times for 95% conversion
dv1 = cm.devol_time(0.1, tbed)     # 0.1 mm diameter
dv2 = cm.devol_time(0.5, tbed)     # 0.5 mm diameter
dv3 = cm.devol_time(1.0, tbed)     # 1.0 mm diameter
dv4 = cm.devol_time(2.0, tbed)     # 2.0 mm diameter
dv_diam = dv1, dv2, dv3, dv4

# Plot
# ----------------------------------------------------------------------------

rct.print_params('Pyrolyzer Parameters', params)

# Plot
# ----------------------------------------------------------------------------

rct.plot_devol_bedtemp(dp, dv_tbed, ('450°C', '500°C', '550°C', '600°C'))
rct.plot_devol_diam(tbed, dv_diam, ('0.1 mm', '0.5 mm', '1 mm', '2 mm'))
rct.show_plots()
