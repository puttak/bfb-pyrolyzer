import chemics as cm


class Bed:

    def __init__(self, params, mug, rhog):
        self.di = params.reactor['di']
        self.dp = params.bed['dp_mean']
        self.dp_min = params.bed['dp_min']
        self.dp_max = params.bed['dp_max']
        self.ep = params.bed['ep']
        self.phi = params.bed['phi']
        self.rhos = params.bed['rho']
        self.zmf = params.bed['zmf']
        self.mug = mug
        self.rhog = rhog

    def calc_umf(self):
        # Conversion for kg/ms = µP * 1e-7
        mug = self.mug * 1e-7
        umf = cm.umf_ergun(self.dp, self.ep, mug, self.phi, self.rhog, self.rhos)
        return umf

    def calc_zexp(self, umf, us):
        fbexp = cm.fbexp(self.di, self.dp, self.rhog, self.rhos, umf, us)
        zexp = self.zmf * fbexp
        return zexp

    def geldart_fig(self, rhog):
        # Conversion for m = µm * 1e6
        # Conversion for g/cm³ = kg/m³ * 0.001
        dp = self.dp * 1e6
        dpmin = self.dp_min * 1e6
        dpmax = self.dp_max * 1e6
        rhog = rhog * 0.001
        rhos = self.rhos * 0.001
        fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
        return fig
