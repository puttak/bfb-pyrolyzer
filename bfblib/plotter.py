import chemics as cm
import matplotlib.pyplot as plt


def _config(ax, xlabel, ylabel):
    ax.grid(color='0.9')
    ax.legend(loc='best')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


def plot_geldart(gas, params, path):
    """
    Plot the Geldart chart for particle size classification.
    """
    # Conversion for m = µm * 1e6
    # Conversion for g/cm³ = kg/m³ * 0.001
    dp = params.bed['dp'] * 1e6
    dpmin = params.bed['dp_min'] * 1e6
    dpmax = params.bed['dp_max'] * 1e6
    rhog = gas.rho * 0.001
    rhos = params.bed['rho'] * 0.001
    fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
    fig.savefig(f'{path}/fig_geldart.pdf')


def plot_intra_particle_heat_cond(bio, path):
    """
    here
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(bio.t, bio.tk[:, 0], lw=2, label='center')
    ax.plot(bio.t, bio.tk[:, -1], lw=2, label='surface')
    ax.axvline(bio.t_ref, c='k', ls='--', label='Tinf')
    _config(ax, 'Time [s]', 'Temperature [K]')
    fig.savefig(f'{path}/fig_intra_hc.pdf')


def plot_umf_temps(tks, umf, tk_ref, path):
    """
    here
    """
    umf_ergun = [x.ergun for x in umf]
    umf_wenyu = [x.wenyu for x in umf]
    ymax = max(umf_ergun + umf_wenyu) * 1.2
    ymin = min(umf_ergun + umf_wenyu) * 0.8

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(tks, umf_ergun, '.-', label='Ergun')
    ax.plot(tks, umf_wenyu, '.-', label="WenYu")
    ax.axvline(tk_ref, color='k', ls='--', label='ref')
    ax.fill_between(tks, umf_ergun, umf_wenyu, alpha=0.6, facecolor='0.9')
    ax.set_ylim(ymin, ymax)
    _config(ax, 'Temperature [K]', 'Min. fluidization velocity, Umf [m/s]')
    fig.savefig(f'{path}/fig_umf_temps.pdf')


def plot_ut_temps(tks, ut_bed, ut_bio, ut_char, path):
    """
    here
    """
    ut_bed_ganser = [x.ganser for x in ut_bed]
    ut_bed_haider = [x.haider for x in ut_bed]
    ut_bio_ganser = [x.ganser for x in ut_bio]
    ut_bio_haider = [x.haider for x in ut_bio]
    ut_char_ganser = [x.ganser for x in ut_char]
    ut_char_haider = [x.haider for x in ut_char]

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(tks, ut_bed_ganser, 'k--', label='Ganser')
    ax.plot(tks, ut_bed_haider, 'k-', label='Haider')
    ax.fill_between(tks, ut_bed_ganser, ut_bed_haider, alpha=0.6, facecolor='khaki', label='bed')
    ax.plot(tks, ut_bio_ganser, 'k--')
    ax.plot(tks, ut_bio_haider, 'k-')
    ax.fill_between(tks, ut_bio_ganser, ut_bio_haider, alpha=0.6, facecolor='lightgreen', label='bio')
    ax.plot(tks, ut_char_ganser, 'k--')
    ax.plot(tks, ut_char_haider, 'k-')
    ax.fill_between(tks, ut_char_ganser, ut_char_haider, alpha=0.6, facecolor='grey', label='char')
    _config(ax, 'Temperature [K]', 'Terminal velocity, Ut [m/s]')
    ax.legend(bbox_to_anchor=(0., 1.02, 1, 0.102), loc=3, ncol=5, mode='expand', frameon=False)
    fig.savefig(f'{path}/fig_ut_temps.pdf')


def plot_tdevol_temps(tks, ts_devol, tk_ref, path):
    """
    here
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(tks, ts_devol, '.-')
    ax.axvline(tk_ref, color='k', ls='--', label='ref')
    _config(ax, 'Temperature [K]', 'Devolatilization time [s]')
    fig.savefig(f'{path}/fig_tdevol_temps.pdf')
