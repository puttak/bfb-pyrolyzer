import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pathlib


def _geldart_data():
    """
    Data points that form demarcation lines and regions on the Geldart chart.
    Points are digitized from Figure 2 in Khawaja 2015.
    """

    acx1 = [20.58, 20.77, 20.96, 20.79, 20.98, 21.17, 21.54, 22.01, 22.78,
            23.57, 24.80, 26.09, 27.80, 29.87, 32.23, 34.92, 38.16, 41.52,
            45.55, 49.98, 54.83, 60.41, 66.84, 73.95, 81.82, 86.43]

    acy1 = [6.60, 5.46, 4.51, 3.68, 3.05, 2.53, 2.11, 1.78, 1.52, 1.29, 1.12,
            0.97, 0.85, 0.76, 0.67, 0.61, 0.55, 0.49, 0.45, 0.41, 0.37, 0.34,
            0.31, 0.29, 0.27, 0.25]

    acx2 = [18.00, 17.86, 17.87, 17.88, 18.05, 18.36, 18.84, 19.33, 20.01,
            20.87, 21.96, 23.30, 24.93, 27.02, 29.27, 31.58, 34.36, 37.39,
            41.02, 45.01, 49.38, 54.64, 60.45, 66.88, 74.00, 77.84]

    acy2 = [5.63, 4.58, 3.76, 3.12, 2.57, 2.16, 1.82, 1.53, 1.31, 1.12, 0.97,
            0.86, 0.76, 0.68, 0.60, 0.54, 0.49, 0.44, 0.40, 0.36, 0.33, 0.30,
            0.28, 0.26, 0.24, 0.23]

    aax = [64.18, 70.99, 78.52, 85.77, 91.00, 94.54, 96.18, 96.23, 95.86,
           94.31, 92.78, 90.89, 87.18, 81.53, 74.66, 67.79, 61.80, 56.81,
           52.44, 49.64, 48.18, 47.36, 46.74, 46.92, 47.09, 47.87, 49.69,
           53.36, 58.03, 64.18]

    aay = [1.22, 1.22, 1.22, 1.18, 1.10, 1.00, 0.91, 0.83, 0.75, 0.67, 0.61,
           0.55, 0.51, 0.47, 0.45, 0.44, 0.45, 0.46, 0.48, 0.52, 0.57, 0.63,
           0.71, 0.79, 0.88, 0.98, 1.07, 1.14, 1.19, 1.22]

    # Combine data points into single line to fill shaded region
    acx = acx1 + acx2[::-1] + [acx1[0]]
    acy = acy1 + acy2[::-1] + [acy1[0]]

    # Equation 6 from Geldart 1973
    d_ab = np.linspace(36, 1068)
    rho_ab = 225 / d_ab

    # Equation 8 from Geldart 1973
    d_bd = np.linspace(380, 2228)
    rho_bd = (10**6) / (d_bd**2)

    return d_ab, rho_ab, d_bd, rho_bd, acx, acy, aax, aay


def geldart_figure(dp, rhog, rhos, dpmin=None, dpmax=None):
    """
    Plot a point on the Geldart chart [Geldart1973]_. Data points for
    demarcation lines and regions were digitized from [Khawaja2015]_.

    Parameters
    ----------
    dp : float
        Sauter mean particle diameter [µm]
    rhog : float
        Gas density [g/cm³]
    rhos : float
        Particle density [g/cm³]
    dpmin : float, optional
        Minimum particle size from particle size distribution [µm]
    dpmax : float, optional
        Max particle size from particle size distribution [µm]

    Returns
    -------
    Matplotlib figure representing Geldart chart and user defined point.

    Note
    ----
    Particle diameter must be in microns (µm) and density in g/cm³.

    References
    ----------
    .. [Geldart1973] D. Geldart. Types of gas fluidization. Powder Technology,
       7, pp. 285-292, 1973.
    .. [Khawaja2015] H.A. Khawaja. Review of the phenomenon of fluidization
       and its numerical modelling techniques. The International Journal of
       Multiphysics, vol. 9, no. 4, pp. 397-407, 2015.
    """

    d_ab, rho_ab, d_bd, rho_bd, acx, acy, aax, aay = _geldart_data()
    rhodiff = rhos - rhog

    fig, ax = plt.subplots(tight_layout=True)

    if dpmin and dpmax is not None:
        low_err = abs(dp - dpmin)
        upper_err = abs(dp - dpmax)
        err = [[low_err], [upper_err]]
        ax.errorbar(dp, rhodiff, fmt='ro', xerr=err, capsize=3)
    else:
        ax.plot(dp, rhodiff, 'ro')

    ax.loglog(d_ab, rho_ab, color='lightsteelblue')
    ax.loglog(d_bd, rho_bd, color='lightsteelblue')
    ax.fill_between(acx, acy, facecolor='lightsteelblue')
    ax.fill_between(aax, aay, facecolor='lightsteelblue')
    ax.text(20, 0.3, 'C\ncohesive', horizontalalignment='center')
    ax.text(68, 0.7, "A'", horizontalalignment='center')
    ax.text(200, 0.4, 'A\naeratable', horizontalalignment='center')
    ax.text(200, 3, 'B\nsand-like', horizontalalignment='center')
    ax.text(1400, 3, 'D\nspoutable', horizontalalignment='center')
    ax.set_xlabel('d$_{\\mathrm{p}}$ [µm]')
    ax.set_ylabel(r'$\mathrm{\rho_s - \rho_g}$ [g/cm³]')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.set_xlim([10, 3000])
    ax.set_xticks([10, 30, 100, 300, 1000, 3000])
    ax.set_ylim([0.1, 10])
    ax.set_yticks([0.1, 0.3, 1, 3, 10])
    ax.grid(color='0.9')
    ax.grid(which='minor', color='0.9')
    ax.tick_params(color='0.7')
    ax.tick_params(which='minor', color='0.7')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))

    return fig


def save_figure(name, fig, cwd):
    """
    here
    """
    results_dir = pathlib.Path(cwd, 'results')
    if not results_dir.exists():
        results_dir.mkdir()
    fig.savefig(f'results/{name}.pdf')
