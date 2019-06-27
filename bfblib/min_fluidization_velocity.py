import chemics as cm


class MinFluidizationVelocity:
    """
    Minimum fluidization velocity (Umf).

    Attributes
    ----------
    attr : float
        Umf value accessable by attribute name.
    """

    def __init__(self, dp, ep, mu, phi, rhog, rhos, *equation):
        self._dp = dp
        self._ep = ep
        self._mu = mu
        self._phi = phi
        self._rhog = rhog
        self._rhos = rhos
        self._equation = equation
        self._calc_umfs()

    def _calc_umfs(self):
        """
        Calculate minimum fluidization velocity from various equations.
        """
        if not self._equation:
            raise ValueError('Must supply name of Umf equation.')

        for eq in self._equation:

            if eq == 'ergun':
                umf = cm.umf_ergun(self._dp, self._ep, self._mu, self._phi, self._rhog, self._rhos)
            elif eq in ('wenyu', 'grace'):
                umf = cm.umf_coeff(self._dp, self._mu, self._rhog, self._rhos, coeff=eq)
            else:
                raise ValueError('Umf equation not available.')

            setattr(self, eq, umf)
