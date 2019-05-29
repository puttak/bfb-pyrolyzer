import numpy as np


class Reactor:

    def __init__(self, params):
        self.di = params.reactor['di']

    @property
    def a_inner(self):
        ai = (np.pi * self.di**2) / 4
        return ai
