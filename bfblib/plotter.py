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
    dp = params.bed['dp'][0] * 1e6
    dpmin = params.bed['dp'][1] * 1e6
    dpmax = params.bed['dp'][2] * 1e6
    rhog = gas.rho * 0.001
    rhos = params.bed['rhos'] * 0.001
    fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
    fig.savefig(f'{path}/fig_geldart.pdf')


def plot_intra_particle_heat_cond(results, path):
    """
    here
    """
    t_hc, tk_hc, t_tkinf = results

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(t_hc, tk_hc[:, 0], lw=2, label='center')
    ax.plot(t_hc, tk_hc[:, -1], lw=2, label='surface')
    ax.axvline(t_tkinf, c='k', ls='--', label='Tinf')
    _config(ax, 'Time [s]', 'Temperature [K]')
    fig.savefig(f'{path}/fig_intra_hc.pdf')


def plot_umf_temps(tks, umfs_ergun, umfs_wenyu, tk_ref, path):
    """
    here
    """
    ymax = max(umfs_ergun + umfs_wenyu) * 1.2
    ymin = min(umfs_ergun + umfs_wenyu) * 0.8

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(tks, umfs_ergun, '.-', label='Ergun')
    ax.plot(tks, umfs_wenyu, '.-', label="WenYu")
    ax.axvline(tk_ref, color='k', ls='--', label='ref')
    ax.fill_between(tks, umfs_ergun, umfs_wenyu, alpha=0.6, facecolor='0.9')
    ax.set_ylim(ymin, ymax)
    _config(ax, 'Temperature [K]', 'Min. fluidization velocity [m/s]')
    fig.savefig(f'{path}/fig_umf_temps.pdf')


def plot_ut_temps(tks, uts_ganser, uts_haider, path):
    """
    here
    """
    uts_bed_ganser = uts_ganser['bed']
    uts_bed_haider = uts_haider['bed']

    uts_bio_ganser = uts_ganser['bio']
    uts_bio_haider = uts_haider['bio']

    uts_char_ganser = uts_ganser['char']
    uts_char_haider = uts_haider['char']

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(tks, uts_bed_ganser, 'k--', label='Ganser')
    ax.plot(tks, uts_bed_haider, 'k-', label='Haider')
    ax.fill_between(tks, uts_bed_ganser, uts_bed_haider, alpha=0.6, facecolor='khaki', label='bed')
    ax.plot(tks, uts_bio_ganser, 'k--')
    ax.plot(tks, uts_bio_haider, 'k-')
    ax.fill_between(tks, uts_bio_ganser, uts_bio_haider, alpha=0.6, facecolor='lightgreen', label='bio')
    ax.plot(tks, uts_char_ganser, 'k--')
    ax.plot(tks, uts_char_haider, 'k-')
    ax.fill_between(tks, uts_char_ganser, uts_char_haider, alpha=0.6, facecolor='grey', label='char')
    _config(ax, 'Temperature [K]', 'Terminal velocity [m/s]')
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
