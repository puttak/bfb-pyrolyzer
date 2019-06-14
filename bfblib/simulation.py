import json
import numpy as np
import textwrap

from .gas import Gas
from .bfb_model import BfbModel


class Simulation:

    def __init__(self, params):
        self.params = params
        self.results = {}
        self.figures = {}
        self.results_case = []

    def run_params(self):

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(**self.params.gas)
        gas.calc_properties()

        # BFB model for fluidization and biomass pyrolysis
        # Matplotlib figures are denoted by the `fig_` prefix
        bfb = BfbModel(gas, self.params.bed, self.params.biomass, self.params.reactor)
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

        print(textwrap.dedent(f"""
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
              Simulate Temperatures
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"""))

        tk_min = self.params.case['tk'][0]
        tk_max = self.params.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        for tk in tks:
            print(f'Running case at {tk} K ...')

            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(**self.params.gas)
            gas.tk = tk
            gas.calc_properties()

            # BFB model for fluidization and biomass pyrolysis
            # Matplotlib figures are denoted by the `fig_` prefix
            bfb = BfbModel(gas, self.params.bed, self.params.biomass, self.params.reactor)
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

    def print_parameters(self):
        """
        Print parameter names, values, and descriptions to terminal.
        """
        params_bed = self.params.bed
        params_biomass = self.params.biomass
        params_gas = self.params.gas
        params_reactor = self.params.reactor

        sp = ', '.join(params_gas['sp'])
        x = ', '.join([str(gx) for gx in params_gas['x']])
        w = 12  # width specifier

        pm_string = f"""
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                   Parameters
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        ------------- Bed --------------\n
        {'dp_mean':<{w}} {params_bed['dp'][0]:<{w}} Mean particle diameter [m]
        {'dp_min':<{w}} {params_bed['dp'][1]:<{w}} Minimum particle diameter [m]
        {'dp_max':<{w}} {params_bed['dp'][2]:<{w}} Maximum particle diameter [m]
        {'ep':<{w}} {params_bed['ep']:<{w}} Void fraction of bed [-]
        {'phi':<{w}} {params_bed['phi']:<{w}} Particle sphericity [-]
        {'rhos':<{w}} {params_bed['rhos']:<{w}} Density of a bed particle [kg/m³]
        {'zmf':<{w}} {params_bed['zmf']:<{w}} Bed height at minimum fluidization [m]

        ----------- Biomass ------------\n
        {'dp_mean':<{w}} {params_biomass['dp_mean']:<{w}} Mean particle diameter [m]
        {'h':<{w}} {params_biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
        {'k':<{w}} {params_biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
        {'mc':<{w}} {params_biomass['mc']:<{w}} Moisture content [%]
        {'sg':<{w}} {params_biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
        {'tk_i':<{w}} {params_biomass['tk_i']:<{w}} Initial particle temperature [K]

        ------------- Gas --------------\n
        {'p':<{w}} {params_gas['p']:<{w},} Gas pressure in reactor [Pa]
        {'q':<{w}} {params_gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
        {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
        {'tk':<{w}} {params_gas['tk']:<{w}} Gas temperature in reactor [K]
        {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

        ------------ Reactor -----------\n
        {'di':<{w}} {params_reactor['di']:<{w}} Inner diameter of reactor [m]
        """
        print(textwrap.dedent(pm_string))

    def print_results(self):
        """
        Print BFB model results to terminal.
        """
        results = self.results
        w = 12  # width specifier

        res_string = f"""
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    Results
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        -------- Gas Properties --------\n
        {'p':<{w}} {results['gas_p']:<{w},} Pressure [Pa]
        {'tk':<{w}} {results['gas_tk']:<{w}} Temperature [K]
        {'mw':<{w}} {results['gas_mw']:<{w}.4f} Molecular weight [g/mol]
        {'mu':<{w}} {results['gas_mu']:<{w}.2f} Viscosity [µP]
        {'rho':<{w}} {results['gas_rho']:<{w}.4f} Density [kg/m³]

        ----------- BFB Model ----------\n
        {'ac':<{w}} {results['ac']:<{w}.4f} Inner cross section area [m²]
        {'us':<{w}} {results['us']:<{w}.4f} Superficial gas velocity [m/s]

        Ergun
        {'umf':<{w}} {results['umf_ergun']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {results['us_umf_ergun']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {results['zexp_ergun']:<{w}.2f} Height of expanded bed [m]

        Wen and Yu
        {'umf':<{w}} {results['umf_wenyu']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {results['us_umf_wenyu']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {results['zexp_wenyu']:<{w}.2f} Height of expanded bed [m]

        {'t_devol':<{w}} {results['t_devol']:<{w}.2f} Devolatilization time for 95% conversion [s]
        {'t_tkinf':<{w}} {results['t_tkinf']:<{w}.2f} Time for particle center to reach T∞ [s]
        """
        print(textwrap.dedent(res_string))

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
