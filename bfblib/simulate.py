import json
import textwrap
from .gas import Gas
from .gas_mix import GasMix
from .bfb_model import BfbModel
import matplotlib.pyplot as plt


class Simulate:

    def __init__(self, params):
        self.params = params
        self.results = {}
        self.figures = {}
        self._run()
        self._print_parameters()
        self._print_results()

    def _run(self):

        # Gas properties
        # Species `sp` in parameters file can be a string for a single gas
        # component or a list for a gas mixture.
        # Note that gas mixture uses the Herning calculation for viscosity.
        sp = self.params.gas['sp']

        if type(sp) is list:
            mus = []
            mws = []
            xs = []
            for i in range(len(sp)):
                gas = Gas(sp[i], self.params.gas['x'][i], self.params)
                mus.append(gas.mu)
                mws.append(gas.mw)
                xs.append(gas.x)
            gas = GasMix(mus, mws, xs, self.params)
            mug = gas.mu_herning
        elif type(sp) is str:
            gas = Gas(sp, self.params.gas['x'], self.params)
            mug = gas.mu

        # BFB model for fluidization and biomass pyrolysis
        # Matplotlib figures are denoted by the `fig_` prefix
        bfb = BfbModel(gas, self.params)
        ac = bfb.calc_inner_ac()
        us = bfb.calc_us(ac)

        umf_ergun = bfb.calc_umf_ergun(mug)
        us_umf_ergun = bfb.calc_us_umf(us, umf_ergun)
        zexp_ergun = bfb.calc_zexp(umf_ergun, us)

        umf_wenyu = bfb.calc_umf_wenyu(mug)
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
            'gas_mu': round(mug, 4),
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

    def _print_parameters(self):
        """
        Print parameter names, values, and descriptions to terminal.
        """
        bed = self.params.bed
        biomass = self.params.biomass
        gas = self.params.gas
        reactor = self.params.reactor

        if type(self.params.gas['sp']) is list:
            sp = ', '.join(self.params.gas['sp'])
            x = ', '.join([str(gx) for gx in self.params.gas['x']])
        else:
            sp = self.params.gas['sp']
            x = self.params.gas['x']

        w = 12  # width specifier

        pm_string = f"""
        <<<<<<<<<< Parameters >>>>>>>>>>

        ------------- Bed --------------\n
        {'dp_mean':<{w}} {bed['dps'][0]:<{w}} Mean particle diameter [m]
        {'dp_min':<{w}} {bed['dps'][1]:<{w}} Minimum particle diameter [m]
        {'dp_max':<{w}} {bed['dps'][2]:<{w}} Maximum particle diameter [m]
        {'ep':<{w}} {bed['ep']:<{w}} Void fraction of bed [-]
        {'phi':<{w}} {bed['phi']:<{w}} Particle sphericity [-]
        {'rhos':<{w}} {bed['rhos']:<{w}} Density of a bed particle [kg/m³]
        {'zmf':<{w}} {bed['zmf']:<{w}} Bed height at minimum fluidization [m]

        ----------- Biomass ------------\n
        {'dp_mean':<{w}} {biomass['dp_mean']:<{w}} Mean particle diameter [m]
        {'h':<{w}} {biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
        {'k':<{w}} {biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
        {'mc':<{w}} {biomass['mc']:<{w}} Moisture content [%]
        {'sg':<{w}} {biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
        {'ti':<{w}} {biomass['ti']:<{w}} Initial particle temperature [K]

        ------------- Gas --------------\n
        {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
        {'p':<{w}} {gas['p']:<{w},} Gas pressure in reactor [Pa]
        {'q':<{w}} {gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
        {'tk':<{w}} {gas['tk']:<{w}} Gas temperature in reactor [K]
        {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

        ------------ Reactor -----------\n
        {'di':<{w}} {reactor['di']:<{w}} Inner diameter of reactor [m]
        """
        print(textwrap.dedent(pm_string))

    def _print_results(self):
        """
        Print BFB model results to terminal.
        """
        w = 12  # width specifier

        res_string = f"""
        <<<<<<<<<<<< Results >>>>>>>>>>>>

        -------- Gas Properties --------\n
        {'p':<{w}} {self.results['gas_p']:<{w},} Pressure [Pa]
        {'tk':<{w}} {self.results['gas_tk']:<{w}} Temperature [K]
        {'mw':<{w}} {self.results['gas_mw']:<{w}.4f} Molecular weight [g/mol]
        {'mu':<{w}} {self.results['gas_mu']:<{w}.2f} Viscosity [µP]
        {'rho':<{w}} {self.results['gas_rho']:<{w}.4f} Density [kg/m³]

        ----------- BFB Model ----------\n
        {'ac':<{w}} {self.results['ac']:<{w}.4f} Inner cross section area [m²]
        {'us':<{w}} {self.results['us']:<{w}.4f} Superficial gas velocity [m/s]

        Ergun
        {'umf':<{w}} {self.results['umf_ergun']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {self.results['us_umf_ergun']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {self.results['zexp_ergun']:<{w}.2f} Height of expanded bed [m]

        Wen and Yu
        {'umf':<{w}} {self.results['umf_wenyu']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {self.results['us_umf_wenyu']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {self.results['zexp_wenyu']:<{w}.2f} Height of expanded bed [m]

        {'t_devol':<{w}} {self.results['t_devol']:<{w}.2f} Devolatilization time for 95% conversion [s]
        {'t_tkinf':<{w}} {self.results['t_tkinf']:<{w}.2f} Time for particle center to reach T∞ [s]
        """
        print(textwrap.dedent(res_string))

    def save_results(self, path):
        """
        Save results as a JSON file to the `results` directory.

        Parameters
        ----------
        path : pathlib.PosixPath
            Path to the `results` directory.
        """
        with open(f'{path}/results.json', 'w') as file:
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
        figs = self.figures
        for name, fig in figs.items():
            fig.savefig(f'{path}/{name}.pdf')

        print('Figures saved to `results` folder.\n')
