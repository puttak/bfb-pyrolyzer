# TODO : put this function in Chemics package


def heatcap(x, T):
    """
    Calculate heat capacity of wood at temperature and moisture content.

    Example:
        cp = heatcap(12, 300)
    Inputs:
        x = moisture content, %
        T = temperature, K
    Output:
        cp_wet = heat capacity wet wood, kJ/(kg*K)

    Reference:
        Glass and Zelinka, 2010. Wood Handbook, Ch. 4, pp. 1-19.
    """

    cpw = 4.18  # heat capacity of water, kJ/(kg*K)

    # coefficients for adjustment factor Ac
    b1 = -0.06191
    b2 = 2.36e-4
    b3 = -1.33e-4

    # adjustment factor for additional energy in wood-water bond, Eq. 4-18
    Ac = x * (b1 + b2 * T + b3 * x)

    # heat capacity of dry wood, Eq. 4-16a, kJ/(kg*K)
    cp_dry = 0.1031 + 0.003867 * T

    # heat capacity of wood that contains water, Eq. 4-17, kJ/(kg*K)
    cp_wet = (cp_dry + cpw * x / 100) / (1 + x / 100) + Ac

    return cp_wet
