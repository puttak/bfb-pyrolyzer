import chemics as cm
import matplotlib.pyplot as plt


def plot_geldart(gas, params, path):
    """
    Plot the Geldart chart for particle size classification.
    """
    # Conversion for m = µm * 1e6
    # Conversion for g/cm³ = kg/m³ * 0.001
    dp = params.bed['dp'][0] * 1e6
    dpmin = params.bed['dp'][1] * 1e6
    dpmax = params.bed['dp'][2] * 1e6
    rhog = gas.rho * 0.001
    rhos = params.bed['rhos'] * 0.001
    fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
    fig.savefig(f'{path}/fig_geldart.pdf')


def plot_intra_particle_heat_cond(particle, path):
    """
    here
    """
    t = particle.t_hc
    tk = particle.tk_hc
    t_tkinf = particle.t_tkinf

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(t, tk[:, 0], lw=2, label='center')
    ax.plot(t, tk[:, -1], lw=2, label='surface')
    ax.axvline(t_tkinf, alpha=0.5, c='k', ls='--', label='Tinf')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Temperature [K]')
    ax.grid(color='0.9')
    ax.legend(loc='best')
    ax.set_frame_on(False)
    ax.tick_params(color='0.9')
    fig.savefig(f'{path}/fig_intra_hc.pdf')
