"""
Geldart particle classification for range of particle diameters and densities.
Fluidization gas is assumed to be nitrogen at 101325 Pa and 773.15 K.
"""

import chemics as cm
import utils

# Parameters
# ----------------------------------------------------------------------------

dp = utils.params.dp
pgas = utils.params.pgas
rhos = utils.params.rhos
tgas = utils.params.tgas

# regions based on bed particle size distribution
# dp in µm and rho in g/cm³
region1 = {'dp_min': 300, 'dp_max': 500, 'rhos_min': 2, 'rhos_max': 2.5}
region2 = {'dp_min': 250, 'dp_max': 425, 'rhos_min': 2, 'rhos_max': 2.5}

# Gas Density for N₂
# ----------------------------------------------------------------------------

mw_n2 = cm.molecular_weight('N2')
rhog = cm.rhog(mw_n2, pgas, tgas)

# Plot Geldart chart
# ----------------------------------------------------------------------------

# Note that 1 g/cm³ is 1000 kg/m³
# Note that 1 m is 1e6 µm

utils.plot_geldart(dp * 1e6, rhog / 1000, rhos / 1000)
utils.plot_geldart_region(rhog / 1000, region1)
utils.plot_geldart_region(rhog / 1000, region2)
utils.show_plots()
