
def thermalcond(x, So, Gb):
    """
    Calculate thermal conductivity of wood at moisture content, volumetric
    shrinkage, and basic specific gravity.

    Example:
        k = thermalcond(12, 12.3, 0.54)
    Inputs:
        x = moisture content, %
        So = volumetric shrinkage, Table 4-3, %
        Gb = basic specific gravity, Table 4-7 or Table 5-3
    Outputs:
        k = thermal conductivity, W/(m*k)

    Reference:
        Glass and Zelinka, 2010. Wood Handbook, Ch. 4, pp. 1-19.
    """

    mcfs = 30   # fiber staturation point estimate, %

    # shrinkage from green to final moisture content, Eq. 4-7, %
    Sx = So * (1 - x / mcfs)

    # specific gravity based on volume at given moisture content, Eq. 4-9
    Gx = Gb / (1 - Sx / 100)

    # thermal conductivity, Eq. 4-15, W/(m*K)
    A = 0.01864
    B = 0.1941
    C = 0.004064
    k = Gx * (B + C * x) + A

    return k
