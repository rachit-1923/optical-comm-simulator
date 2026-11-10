import numpy as np
class Receiver:
    def __init__(self, sens=-20.0): self.sens = sens
    def check_link_margin(self, rx): return rx - self.sens
    def add_awgn_noise(self, s, snr_db):
        p = np.mean(np.abs(s)**2)
        if p==0: return s
        n_p = p / (10**(snr_db/10.0))
        if np.iscomplexobj(s): return s + np.sqrt(n_p/2)*(np.random.randn(len(s)) + 1j*np.random.randn(len(s)))
        return s + np.sqrt(n_p)*np.random.randn(len(s))
