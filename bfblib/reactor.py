import numpy as np


class Reactor:

    def __init__(self, params):
        self.di = params.reactor['di']

    def calc_ai(self):
        ai = (np.pi * self.di**2) / 4
        return ai
