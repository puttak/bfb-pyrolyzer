import json
import numpy as np
from .gas import Gas
from .bfb_model import BfbModel


class Simulation:

    def __init__(self, params):
        self.params_case = params.case
        self.params_bed = params.bed
        self.params_biomass = params.biomass
        self.params_gas = params.gas
        self.params_reactor = params.reactor
        self.results = {}
        self.figures = {}
        self.results_case = []

    def run_params(self):

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(**self.params_gas)
        gas.calc_properties()

        # BFB model for fluidization and biomass pyrolysis
        # Matplotlib figures are denoted by the `fig_` prefix
        bfb = BfbModel(gas, self.params_bed, self.params_biomass, self.params_reactor)
        ac = bfb.calc_inner_ac()
        us = bfb.calc_us(ac)

        umf_ergun = bfb.calc_umf_ergun(gas.mu)
        us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
        zexp_ergun = bfb.calc_zexp(umf_ergun, us)

        umf_wenyu = bfb.calc_umf_wenyu(gas.mu)
        us_umf_wenyu = bfb.calc_us_umf(us, umf_wenyu)
        zexp_wenyu = bfb.calc_zexp(umf_wenyu, us)

        t_hc = bfb.build_time_vector()
        tk_hc = bfb.calc_trans_hc(t_hc, gas.tk)
        t_tkinf = bfb.calc_time_tkinf(t_hc, tk_hc)
        t_devol = bfb.calc_devol_time()

        fig_geldart = bfb.build_geldart_figure()
        fig_heatcond = bfb.build_heat_cond_figure(t_hc, tk_hc, t_tkinf)

        # Store results from calculations
        self.results = {
            'gas_p': gas.p,
            'gas_tk': gas.tk,
            'gas_mw': round(gas.mw, 4),
            'gas_mu': round(gas.mu, 4),
            'gas_rho': round(gas.rho, 4),
            'ac': round(ac, 4),
            'us': round(us, 4),
            'umf_ergun': round(umf_ergun, 4),
            'us_umf_ergun': round(us_umf_ergun, 4),
            'zexp_ergun': round(zexp_ergun, 4),
            'umf_wenyu': round(umf_wenyu, 4),
            'us_umf_wenyu': round(us_umf_wenyu, 4),
            'zexp_wenyu': round(zexp_wenyu, 4),
            't_tkinf': round(t_tkinf, 4),
            't_devol': round(t_devol, 4)
        }

        # Store plot figures
        self.figures = {
            'geldart': fig_geldart,
            'heatcond': fig_heatcond
        }

    def run_temps(self):

        tk_min = self.params_case['tk'][0]
        tk_max = self.params_case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        for tk in tks:
            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(**self.params_gas)
            gas.tk = tk
            gas.calc_properties()

            # BFB model for fluidization and biomass pyrolysis
            # Matplotlib figures are denoted by the `fig_` prefix
            bfb = BfbModel(gas, self.params_bed, self.params_biomass, self.params_reactor)
            ac = bfb.calc_inner_ac()
            us = bfb.calc_us(ac)

            umf_ergun = bfb.calc_umf_ergun(gas.mu)
            us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
            zexp_ergun = bfb.calc_zexp(umf_ergun, us)

            umf_wenyu = bfb.calc_umf_wenyu(gas.mu)
            us_umf_wenyu = bfb.calc_us_umf(us, umf_wenyu)
            zexp_wenyu = bfb.calc_zexp(umf_wenyu, us)

            t_hc = bfb.build_time_vector()
            tk_hc = bfb.calc_trans_hc(t_hc, gas.tk)
            t_tkinf = bfb.calc_time_tkinf(t_hc, tk_hc)
            t_devol = bfb.calc_devol_time()

            # Store results from calculations
            self.results_case.append({
                'gas_p': gas.p,
                'gas_tk': gas.tk,
                'gas_mw': round(gas.mw, 4),
                'gas_mu': round(gas.mu, 4),
                'gas_rho': round(gas.rho, 4),
                'ac': round(ac, 4),
                'us': round(us, 4),
                'umf_ergun': round(umf_ergun, 4),
                'us_umf_ergun': round(us_umf_ergun, 4),
                'zexp_ergun': round(zexp_ergun, 4),
                'umf_wenyu': round(umf_wenyu, 4),
                'us_umf_wenyu': round(us_umf_wenyu, 4),
                'zexp_wenyu': round(zexp_wenyu, 4),
                't_tkinf': round(t_tkinf, 4),
                't_devol': round(t_devol, 4)
            })

    def save_results(self, path, case=False):
        """
        Save results as a JSON file to the `results` directory.

        Parameters
        ----------
        path : pathlib.PosixPath
            Path to the `results` directory.
        """
        with open(f'{path}/results.json', 'w') as file:
            if case:
                file.write(json.dumps(self.results_case, indent=4))
            else:
                file.write(json.dumps(self.results, indent=4))

        print('Results saved to `results` folder.\n')

    def save_figures(self, path):
        """
        Save figures as PDF files to the `results` directory.

        Parameters
        ----------
        path : pathlib.PosixPath
            Path to the `results` directory.
        """
        for name, fig in self.figures.items():
            fig.savefig(f'{path}/{name}.pdf')

        print('Figures saved to `results` folder.\n')
