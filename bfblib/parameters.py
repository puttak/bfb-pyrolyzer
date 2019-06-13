from dataclasses import dataclass


@dataclass
class BedParams:
    __slots__ = 'dps', 'ep', 'phi', 'rhos', 'zmf'
    dps: tuple
    ep: float
    phi: float
    rhos: float
    zmf: float


@dataclass
class BiomassParams:
    __slots__ = 'dp_mean', 'h', 'k', 'mc', 'sg', 'tk_i', 'b', 'm', 'nt', 't_max'
    dp_mean: float
    h: float
    k: float
    mc: float
    sg: float
    tk_i: float
    b: int
    m: int
    nt: int
    t_max: int


@dataclass
class CaseParams:
    __slots__ = 'p', 'q', 'tk'
    p: tuple
    q: tuple
    tk: tuple


@dataclass
class GasParams:
    __slots__ = 'p', 'q', 'tk', 'sp', 'x'
    p: float
    q: float
    tk: float
    sp: list
    x: list


@dataclass
class ReactorParams:
    __slots__ = 'di'
    di: float
