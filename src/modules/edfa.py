import numpy as np
from src.core.utils import dbm_to_linear, linear_to_dbm
from src.core.constants import H, C

class EDFA:
    def __init__(self, g0_db=20.0, psat_dbm=15.0, nf_db=5.0, wl_nm=1550.0):
        self.g0, self.psat, self.nf, self.wl = g0_db, psat_dbm, nf_db, wl_nm*1e-9
    def amplify(self, pin_dbm):
        p_in, p_sat, g0_lin = dbm_to_linear(pin_dbm), dbm_to_linear(self.psat), 10**(self.g0/10.0)
        g_lin = g0_lin / (1 + p_in/p_sat)
        return linear_to_dbm(p_in * g_lin), 10*np.log10(g_lin)
    def calculate_ase_noise(self, g_db, b_hz=12.5e9):
        return (10**(self.nf/10.0)/2.0) * (10**(g_db/10.0) - 1) * H * (C/self.wl) * b_hz
