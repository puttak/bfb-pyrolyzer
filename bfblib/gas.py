import chemics as cm


class Gas:

    def __init__(self, sp, x, p, t):
        self.sp = sp
        self.x = x
        self.p = p
        self.t = t
        self.mw = cm.mw(sp)

    def calc_mu(self):
        mu_gas = cm.mu_gas(self.sp, self.t)
        return mu_gas

    def calc_rho(self):
        rho_gas = cm.rhog(self.mw, self.p, self.t)
        return rho_gas

    def calc_us(self, a_inner, q_slm):
        p_kPa = self.p / 1000
        q_lpm = cm.slm_to_lpm(q_slm, p_kPa, self.t)
        q_m3s = q_lpm / 60_000
        us_gas = q_m3s / a_inner
        return us_gas


class GasMix:

    def __init__(self, mus, mws, xs, p, t):
        self.mus = mus
        self.mws = mws
        self.xs = xs
        self.p = p
        self.t = t

    def calc_mu(self, method):
        if method == 'graham':
            mu_mix = cm.mu_graham(self.mus, self.xs)
        elif method == 'herning':
            mu_mix = cm.mu_herning(self.mus, self.mws, self.xs)
        return mu_mix

    def calc_mw(self):
        mw_mix = cm.mw_mix(self.mws, self.xs)
        return mw_mix

    def calc_rho(self, mw_mix):
        rho_mix = cm.rhog(mw_mix, self.p, self.t)
        return rho_mix
