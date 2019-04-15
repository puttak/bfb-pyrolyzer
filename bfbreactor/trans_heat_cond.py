import numpy as np
import scipy.linalg as sp
from .heat_cap import heatcap


def hc2(d, x, k, Gb, h, Ti, Tinf, b, m, t):
    """
    1D transient heat conduction for biomass particle pyrolysis with convection
    at surface, symmetry at center, k = constant and Cp(x, T).
    Returns array of temperatures [T] at each intraparticle node point.

    Solves system of equations [A]*[x] = [b] where:
    A = known coefficent matrix, tridiagonal for 1-D problem
    x = unknown vector, next temperature at each node
    b = known vector, current temperature at each node

    Example:
        T = hc(d, rho, x, So, Gb, h, Ti, Tinf, b, m, t)
    Inputs:
        d = particle diameter, m (e-6 for microns, e-3 for mm)
        x = moisture content, %
        Gb = basic specific gravity, Wood Handbook Table 4-7
        h = heat transfer coefficient, W/m^2*K
        Ti = initial particle temp, K
        Tinf = ambient temperature, K
        b = shape factor where 2 is sphere, 1 is cylinder, 0 is slab
        m = number of nodes from center (m=0) to surface (m)
        t = time vector, s
    Output:
        T = temperature array, K
    """

    # Setup parameters for the system of equations and arrays to store the
    # temperatures [T] and time vector [t]
    # -------------------------------------------------------------------------

    nr = m - 1            # number of radius steps
    r = d / 2             # radius of particle, m
    dr = r / nr           # radius step as delta r, m

    tmax = t.max()      # max time, s
    nt = len(t) - 1     # number of time steps
    dt = tmax / nt      # time step as delta t, s

    # temperature array [T], first row is initial temperatures Ti of the solid
    # row = time step, column = node point from 0 (center) to M (surface)
    T = np.zeros((len(t), m))
    T[0] = Ti

    # vectors = cp, alpha, Fo whereas single values = rho, k, Bi
    rho = Gb * 1000
    cp = heatcap(x, T[0]) * 1000
    alpha = k / (rho * cp)
    Fo = alpha * dt / (dr**2)
    Bi = h * dr / k

    # Solve system of equations [A]*[x] = [b] as a banded matrix with SciPy
    # See the url below for documentation on scipy.linalg.solve_banded
    # http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.linalg.solve_banded.html
    # -------------------------------------------------------------------------
    # * Note the following Python rules when indexing lists and arrays.
    #   Given b = [0, 1, 2, 3, 4, 5]
    #   b[4] = 4            returns the item in b at index 4
    #   b[1:4] = [1, 2, 3]  returns items in b at indices 1 to 3 excluding 4

    # create banded matrix [ab] that holds the tridiagonal matrix from [A]
    ab = np.zeros((3, m))

    # range for internal nodes that apply to upper & lower diagonals of [A]
    j = np.arange(1, m - 1)

    # upper diagonal from coefficient array [A] as first row of [ab]
    ab[0, 1] = -2 * (1 + b) * Fo[0]                 # center node from [A], i=0
    ab[0, 2:] = -Fo[1:m - 1] * (1 + b / (2 * j))    # internal nodes from [A], i=1..M-1

    # center diagonal from coefficient array [A] as second row of [ab]
    ab[1, 0] = 1 + 2 * (1 + b) * Fo[0]                                  # center node from [A], i=0
    ab[1, 1:m - 1] = 1 + 2 * Fo[1:m - 1]                                # internal nodes from [A], i=1..M-1
    ab[1, m - 1] = 1 + 2 * Fo[m - 1] * (1 + Bi + (b / (2 * m)) * Bi)    # surface node from [A], i=M

    # lower diagonal from ceofficient array [A] as third row of [ab]
    ab[2, 0:m - 2] = -Fo[1:m - 1] * (1 - b / (2 * j))   # internal nodes from [A], i=1..M-1
    ab[2, m - 2] = -2 * Fo[m - 1]                       # surface node from [A], i=M

    # create column vector [bb] as the known vector [b]
    bb = np.zeros(m)    # initialize vector
    bb[0] = Ti          # initial center temperature, T0
    bb[1:m - 1] = Ti    # initial internal tempratures, T1...Tm-1
    bb[m - 1] = Ti + 2 * Fo[m - 1] * Bi * (1 + b / (2 * m)) * Tinf  # initial surface temperature Tm

    # solve T at each time step using scipy.linalg.solve_banded
    # T[i] is temperatures at each node for time step i
    # then update properties and [bb] from new temperatures
    for i in range(1, nt + 1):
        T[i] = sp.solve_banded((1, 1), ab, bb)

        # update heat capacity, alpha, and Fourier number
        cp = heatcap(x, T[i]) * 1000
        alpha = k / (rho * cp)
        Fo = alpha * dt / (dr**2)

        # update banded matrix [ab]
        ab[0, 1] = -2 * (1 + b) * Fo[0]
        ab[0, 2:] = -Fo[1:m - 1] * (1 + b / (2 * j))

        ab[1, 0] = 1 + 2 * (1 + b) * Fo[0]
        ab[1, 1:m - 1] = 1 + 2 * Fo[1:m - 1]
        ab[1, m - 1] = 1 + 2 * Fo[m - 1] * (1 + Bi + (b / (2 * m)) * Bi)

        ab[2, 0:m - 2] = -Fo[1:m - 1] * (1 - b / (2 * j))
        ab[2, m - 2] = -2 * Fo[m - 1]

        # update column vector [bb]
        bb = T[i].copy()
        bb[m - 1] = T[i, m - 1] + 2 * Fo[m - 1] * Bi * (1 + b / (2 * m)) * Tinf

    # return temperature array [T] in Kelvin
    return T


def hc(m, dr, b, dt, h, Tinf, g, T, r, pbar, cpbar, kbar):
    """
    1D transient heat conduction within a solid sphere, cylinder, or slab shape
    with convection at the surface and symmetry at center. Returns an array of
    temperatures [T] at each intraparticle node point.

    Solves system of equations [A]*[x] = [b] where:
    A = known coefficent matrix, tridiagonal for 1-D problem
    x = unknown vector, next temperature at each node
    b = known vector, current temperature at each node

    Example:
    T = hc(m, dr, b, dt, h, Tinf, g, T, i, r, pbar, cpbar, kbar)

    where:
    m = number of nodes from center (m=0) to surface (m)
    dr = radius step, m
    b = shape factor where 2 is sphere, 1 is cylinder, 0 is slab
    dt = time step, s
    h = heat transfer coefficient, W/m^2*K
    Tinf = ambient temperature, K
    g = heat generation
    T = temperature at node
    i = time index
    r = radius of particle, m
    pbar = effective density or concentration
    cpbar = effective heat capacity, J/kg*K
    kbar = effective thermal conductivity, W/m*K
    """

    ab = np.zeros((3, m))   # banded array from the tridiagonal matrix
    bb = np.zeros(m)        # column vector

    k = np.arange(1, m - 1)
    ri = (k * dr)**b
    rminus12 = ((k - 0.5) * dr)**b
    rplus12 = ((k + 0.5) * dr)**b

    v = dt / (pbar[0] * cpbar[0])

    # create internal terms
    kminus12 = (kbar[k] + kbar[k - 1]) / 2
    kplus12 = (kbar[k] + kbar[k + 1]) / 2
    w = dt / (pbar[k] * cpbar[k] * ri * (dr**2))
    z = dt / (pbar[k] * cpbar[k])

    # create surface terms
    ww = dt / (pbar[m - 1] * cpbar[m - 1])
    krminus12 = (kbar[m - 1] + kbar[m - 2]) / 2

    # upper diagonal
    ab[0, 1] = -(2 * v * kbar[0] * (1 + b)) / (dr**2)   # center node T1
    ab[0, 2:] = -w * rplus12 * kplus12                  # internal nodes Tm+1

    # center diagonal
    ab[1, 0] = 1 + (2 * v * kbar[0] * (1 + b)) / (dr**2)                                # center node T0
    ab[1, 1:m - 1] = 1 + w * rminus12 * kminus12 + w * rplus12 * kplus12                # internal nodes Tm
    ab[1, m - 1] = 1 + (2 * ww / (dr**2)) * krminus12 + ww * ((2 / dr) + (b / r)) * h   # surface node Tr

    # lower diagonal
    ab[2, 0:m - 2] = -w * rminus12 * kminus12       # internal nodes Tm-1
    ab[2, m - 2] = -(2 * ww / (dr**2)) * krminus12  # surface node Tr-1

    # column vector
    bb[0] = T[0] + v * g[0]                                                         # center node T0
    bb[1:m - 1] = T[k] + z * g[k]                                                   # internal nodes Tm
    bb[m - 1] = T[m - 1] + ww * ((2 / dr) + (b / r)) * h * Tinf + ww * g[m - 1]     # surface node Tr

    # temperatures
    T = sp.solve_banded((1, 1), ab, bb)

    return T
