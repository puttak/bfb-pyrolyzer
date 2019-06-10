import chemics as cm
import matplotlib.pyplot as plt
import pathlib


def plot_geldart(gas, params):
    # Conversion for m = µm * 1e6
    # Conversion for g/cm³ = kg/m³ * 0.001
    dp = params.bed['dps'][0] * 1e6
    dpmin = params.bed['dps'][1] * 1e6
    dpmax = params.bed['dps'][2] * 1e6
    rhog = gas.rho * 0.001
    rhos = params.bed['rhos'] * 0.001
    fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
    return fig


def plot_heat_cond(t, tk, t_tkinf):
    """
    here
    """
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
    return fig


def save_figures(cwd, figs):
    """
    Save figures as a PDF to the `results` directory.

    Parameters
    ----------
    cwd : pathlib.PosixPath
        Path to current working directory.
    figs : dict
        Each key is used to name file. Each value is a Matplotlib figure.
    """
    results_dir = pathlib.Path(cwd, 'results')
    if not results_dir.exists():
        results_dir.mkdir()

    for name, fig in figs.items():
        fig.savefig(f'results/{name}.pdf')

    print('Plot figures saved to `results` folder.\n')
