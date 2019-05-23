"""
Basic calculations related to pyrolyzer.
"""

import chemics as cm
import numpy as np
from utils import params

# Parameters
# ----------------------------------------------------------------------------

di = params.di
p_gas = params.pgas
t_gas = params.tgas

# Calculations for N2 gas
# ----------------------------------------------------------------------------

a_in = (np.pi * di**2) / 4

q_lpm = cm.slm_to_lpm(14, p_gas / 1000, t_gas)
q_m3s = q_lpm / 60_000

u_gas = q_m3s / a_in
u_umf = u_gas / 0.05

# Print
# ----------------------------------------------------------------------------

print(f"""
a_in \t {a_in:.4f} \t m² \t inner cross section area of reactor
q_lpm \t {q_lpm:.4f} \t LPM \t gas flow
q_m3s \t {q_m3s:.4g} \t m³/s \t gas flow
u_gas \t {u_gas:.4f} \t m/s \t gas velocity
u/umf \t {u_umf:.4f} \t -- \t u over umf
""")
